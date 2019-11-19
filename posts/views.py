from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.models import UserFeed, UserNotification, UserReport
from posts.models import Post, PostHashtag, Comment, Like, CommentLike
from posts.serializers import PostSerializer, PostCommentSerializer

from base64 import b64decode
import datetime

from apns import APNs, Payload

from reach.settings import APNS_CERF_PATH, APNS_CERF_SANDBOX_MODE, PAGE_OFFSET

@api_view(["POST"])
def add_new_post(request):
    """
Add new post method.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "text": "Some post text here...",
        "image": "somebase64stringhere",
        "permission": true,
        "hashtags": ["first", "second", "third"]
    }

    Code statuses can be found here: /api/v1/docs/status-code/

    Success json:
    {
        "success": <status_code>,
        "post": {
            "id": 11,
            "author": {
                "id": 2,
                "username": "antonboksha",
                "first_name": "",
                "last_name": "",
                "email": "antonboksha@gmail.com",
                "info": {
                    "full_name": "",
                    "biography": "qweqweqwe",
                    "like_count": 0,
                    "comment_count": 0,
                    "rate": 10,
                    "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                    "is_facebook": false,
                    "is_twitter": false,
                    "is_instagram": false
                },
                "count_downvoted": 1,
                "count_upvoted": 1,
                "count_likes": 1,
                "count_comments": 2,
                "complete_likes": 50
            },
            "text": "here we fucking go!2",
            "like_count": 0,
            "comment_count": 0,
            "date": "2015-11-23T10:44:28.217756Z",
            "permission": true,
            "image": "/media/default_images/default.png",
            "post_hashtags": [
                {
                    "id": 7,
                    "hashtag": "first"
                },
                {
                    "id": 8,
                    "hashtag": "second"
                },
                {
                    "id": 9,
                    "hashtag": "third"
                }
            ],
            "post_comments": [
            {
                "id": 1,
                "text": "Some post text here...",
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 0,
                        "avatar": "/media/default_images/default.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 1,
                    "complete_likes": 50
                },
                "date": "2015-11-23T16:21:24.335014Z",
                "rate": 0,
                "is_upvoted": false,
                "is_downvoted": false,
                "best_response": false
            },
            {
                "id": 2,
                "text": "Some post text here...",
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 0,
                        "avatar": "/media/default_images/default.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 1,
                    "complete_likes": 50
                },
                "date": "2015-11-23T16:23:42.295629Z",
                "rate": 0,
                "is_upvoted": false,
                "is_downvoted": false,
                "best_response": false
            }],
            "like_count": 0,
            "comment_count": 0
        }
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                if "text" in request.data and request.data["text"] != "" and request.data["text"] is not None:
                    if len(request.data["text"]) < 1:
                        return Response({"error": 21})
                    elif len(request.data["text"]) > 10000:
                        return Response({"error": 22})
                    else:
                        token = get_object_or_404(Token, key=request.data["token"])
                        post = Post.objects.create(permission=request.data["permission"],
                                                   author_id=token.user_id,
                                                   text=request.data["text"])
                        if "image" in request.data and request.data["image"] != "" \
                                and request.data["image"] is not None:
                            image_data = b64decode(request.data["image"])
                            post.image = ContentFile(image_data, "post.png")
                            post.save()
                        if "hashtags" in request.data and len(request.data["hashtags"]) > 0:
                            for hashtag in request.data["hashtags"]:
                                PostHashtag.objects.create(post=post,
                                                           hashtag=hashtag)
                        serializer = PostSerializer(post, context={'user_id': token.user_id})
                        return Response({"success": 23,
                                         "post": serializer.data})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def add_new_comment(request):
    """
Add new comment method.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "text": "Some post text here...",
        "post_id": 1,
        "permission": true
    }

    Code statuses can be found here: /api/v1/docs/status-code/

    Success json:
    {
        "success": <status_code>,
        "post": {
            "id": 11,
            "author": {
                "id": 2,
                "username": "antonboksha",
                "first_name": "",
                "last_name": "",
                "email": "antonboksha@gmail.com",
                "info": {
                    "full_name": "",
                    "biography": "qweqweqwe",
                    "like_count": 0,
                    "comment_count": 0,
                    "rate": 10,
                    "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                    "is_facebook": false,
                    "is_twitter": false,
                    "is_instagram": false
                },
                "count_downvoted": 1,
                "count_upvoted": 1,
                "count_likes": 1,
                "count_comments": 2,
                "complete_likes": 50
            },
            "text": "here we fucking go!2",
            "like_count": 0,
            "comment_count": 0,
            "date": "2015-11-23T10:44:28.217756Z",
            "permission": true,
            "image": "/media/default_images/default.png",
            "post_hashtags": [
                {
                    "id": 7,
                    "hashtag": "first"
                },
                {
                    "id": 8,
                    "hashtag": "second"
                },
                {
                    "id": 9,
                    "hashtag": "third"
                }
            ],
            "post_comments": [
            {
                "id": 1,
                "text": "Some post text here...",
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 0,
                        "avatar": "/media/default_images/default.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 1,
                    "complete_likes": 50
                },
                "date": "2015-11-23T16:21:24.335014Z",
                "permission": true,
                "rate": 0,
                "is_upvoted": false,
                "is_downvoted": false,
                "best_response": false
            },
            {
                "id": 2,
                "text": "Some post text here...",
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 0,
                        "avatar": "/media/default_images/default.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 1,
                    "complete_likes": 50
                },
                "date": "2015-11-23T16:23:42.295629Z",
                "permission": true,
                "rate": 0,
                "is_upvoted": false,
                "is_downvoted": false,
                "best_response": false
            }],
            "like_count": 0,
            "comment_count": 0,
        }
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                if "text" in request.data and request.data["text"] != "" and request.data["text"] is not None:
                    if len(request.data["text"]) < 10:
                        return Response({"error": 24})
                    elif len(request.data["text"]) > 255:
                        return Response({"error": 25})
                    else:
                        if "post_id" in request.data and request.data["post_id"] != "" and \
                                        request.data["post_id"] is not None:
                            if type(request.data["post_id"]) is int:
                                if Post.objects.filter(pk=request.data["post_id"]).exists():
                                    token = get_object_or_404(Token, key=request.data["token"])
                                    post = get_object_or_404(Post, pk=request.data["post_id"])
                                    comment = Comment.objects.create(post=post,
                                                                     author_id=token.user_id,
                                                                     text=request.data["text"],
                                                                     permission=request.data["permission"])
                                    serializer = PostSerializer(post, context={'user_id': token.user_id})
                                    if request.data["permission"]:
                                        UserFeed.objects.create(user=post.author,
                                                                action_user=token.user,
                                                                post_comment=comment,
                                                                action="PostComment")
                                        message = "{} commented on your post".format(token.user.username)
                                    else:
                                        message = "Anonymous commented on your post"
                                    if post.author != token.user:
                                        custom = {
                                            "post_id": post.id
                                        }
                                        apns = APNs(use_sandbox=APNS_CERF_SANDBOX_MODE, cert_file=APNS_CERF_PATH)
                                        payload = Payload(alert=message, sound="default", category="TEST", badge=1, custom=custom)
                                        user_notifications = UserNotification.objects.filter(user=post.author)
                                        for user_notification in user_notifications:
                                            try:
                                                apns.gateway_server.send_notification(user_notification.device_token, payload)
                                            except:
                                                pass
                                    return Response({"success": 26,
                                                     "post": serializer.data})
                                else:
                                    return Response({"error": 27})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def get_user_posts(request):
    """
Get user all posts method.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "offset": 0
    }

    Code statuses can be found here: /api/v1/docs/status-code/

    Success json:
    {
        "post": [
            {
                "id": 1,
                author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "qweqweqwe",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 10,
                        "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 2,
                    "complete_likes": 50
                },
                "text": "Some post text here...",
                "like_count": 0,
                "comment_count": 0,
                "date": "2015-11-23T16:19:47.570547Z",
                "permission": true,
                "image": "/media/post/4a62f3f2-e4e2-4085-982d-cdb57c0f7ca3.png",
                "post_hashtags": [
                    {
                        "id": 1,
                        "hashtag": "first"
                    },
                    {
                        "id": 2,
                        "hashtag": "second"
                    },
                    {
                        "id": 3,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [
                    {
                        "id": 1,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:21:24.335014Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    },
                    {
                        "id": 2,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:23:42.295629Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    },
                    {
                        "id": 3,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:24:03.634480Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    },
                    {
                        "id": 4,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:24:05.060450Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    }
                ],
                "like_count": 0,
                "comment_count": 0
            },
            {
                "id": 2,
                "text": "Some post text here...",
                "like_count": 0,
                "comment_count": 0,
                "date": "2015-11-23T16:40:39.438305Z",
                "permission": true,
                "image": "/media/post/5f7f8233-7704-4634-b366-6082c3cfbabe.png",
                "post_hashtags": [
                    {
                        "id": 4,
                        "hashtag": "first"
                    },
                    {
                        "id": 5,
                        "hashtag": "second"
                    },
                    {
                        "id": 6,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [],
                "like_count": 0,
                "comment_count": 0
            }
        ],
        "success": 29,
        "offset": 10
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                token = get_object_or_404(Token, key=request.data["token"])
                start_offset = request.data["offset"]
                end_offset = start_offset + PAGE_OFFSET
                posts = Post.objects.all().order_by("-date")[start_offset:end_offset]
                serializer = PostSerializer(posts, many=True, context={'user_id': token.user_id})
                return Response({"success": 29,
                                 "post": serializer.data,
                                 "offset": end_offset})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def send_like(request):
    """
Send like to posts.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "post_id": 12
    }

    Code statuses can be found here: /api/v1/docs/status-code/

    Success json:
    {
        "post": [
            {
                "id": 1,
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "qweqweqwe",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 10,
                        "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 2,
                    "complete_likes": 50
                },
                "text": "Some post text here...",
                "like_count": 0,
                "comment_count": 0,
                "date": "2015-11-23T16:19:47.570547Z",
                "permission": true,
                "image": "/media/post/4a62f3f2-e4e2-4085-982d-cdb57c0f7ca3.png",
                "post_hashtags": [
                    {
                        "id": 1,
                        "hashtag": "first"
                    },
                    {
                        "id": 2,
                        "hashtag": "second"
                    },
                    {
                        "id": 3,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [
                    {
                        "id": 1,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:21:24.335014Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    },
                    {
                        "id": 2,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:23:42.295629Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    },
                    {
                        "id": 3,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:24:03.634480Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    },
                    {
                        "id": 4,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:24:05.060450Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    }
                ],
                "like_count": 0,
                "comment_count": 0
            },
            {
                "id": 2,
                "text": "Some post text here...",
                "like_count": 0,
                "comment_count": 0,
                "date": "2015-11-23T16:40:39.438305Z",
                "permission": true,
                "image": "/media/post/5f7f8233-7704-4634-b366-6082c3cfbabe.png",
                "post_hashtags": [
                    {
                        "id": 4,
                        "hashtag": "first"
                    },
                    {
                        "id": 5,
                        "hashtag": "second"
                    },
                    {
                        "id": 6,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [],
                "like_count": 0,
                "comment_count": 0
            }
        ],
        "success": True
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                token = get_object_or_404(Token, key=request.data["token"])
                if Post.objects.filter(pk=request.data["post_id"]).exists():
                    post = Post.objects.get(pk=request.data["post_id"])
                    if Like.objects.filter(post=post, user_id=token.user_id).exists():
                        return Response({"error": 31})
                    else:
                        post.count_likes += 1
                        post.save()
                        like = Like.objects.create(post=post, user_id=token.user_id)
                        serializer = PostSerializer(post, context={'user_id': token.user_id})
                        UserFeed.objects.create(user=post.author,
                                                action_user=token.user,
                                                like=like,
                                                action="Like")
                        if post.author != token.user:
                            message = "{} like your post".format(token.user.username)
                            custom = {
                                "post_id": post.id
                            }
                            apns = APNs(use_sandbox=APNS_CERF_SANDBOX_MODE, cert_file=APNS_CERF_PATH)
                            payload = Payload(alert=message, sound="default", category="TEST", badge=1, custom=custom)
                            user_notifications = UserNotification.objects.filter(user=post.author)
                            for user_notification in user_notifications:
                                try:
                                    apns.gateway_server.send_notification(user_notification.device_token, payload)
                                except:
                                    pass
                        return Response({"success": 30,
                                         "post": serializer.data})
                else:
                    return Response({"error": 32})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def remove_like(request):
    """
Remove like to posts.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "post_id": 12
    }

    Code statuses can be found here: /api/v1/docs/status-code/

    Success json:
    {
        "post": [
            {
                "id": 1,
                "text": "Some post text here...",
                "like_count": 0,
                "comment_count": 0,
                "date": "2015-11-23T16:19:47.570547Z",
                "permission": true,
                "image": "/media/post/4a62f3f2-e4e2-4085-982d-cdb57c0f7ca3.png",
                "post_hashtags": [
                    {
                        "id": 1,
                        "hashtag": "first"
                    },
                    {
                        "id": 2,
                        "hashtag": "second"
                    },
                    {
                        "id": 3,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [
                    {
                        "id": 1,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:21:24.335014Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    },
                    {
                        "id": 2,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:23:42.295629Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    },
                    {
                        "id": 3,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:24:03.634480Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    },
                    {
                        "id": 4,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:24:05.060450Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    }
                ],
                "like_count": 0,
                "comment_count": 0
            },
            {
                "id": 2,
                "text": "Some post text here...",
                "like_count": 0,
                "comment_count": 0,
                "date": "2015-11-23T16:40:39.438305Z",
                "permission": true,
                "image": "/media/post/5f7f8233-7704-4634-b366-6082c3cfbabe.png",
                "post_hashtags": [
                    {
                        "id": 4,
                        "hashtag": "first"
                    },
                    {
                        "id": 5,
                        "hashtag": "second"
                    },
                    {
                        "id": 6,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [],
                "like_count": 0,
                "comment_count": 0
            }
        ],
        "success":
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                token = get_object_or_404(Token, key=request.data["token"])
                if Post.objects.filter(pk=request.data["post_id"]).exists():
                    post = Post.objects.get(pk=request.data["post_id"])
                    if Like.objects.filter(post=post, user_id=token.user_id).exists():
                        post.count_likes -= 1
                        post.save()
                        Like.objects.filter(post=post, user_id=token.user_id).delete()
                        serializer = PostSerializer(post, context={'user_id': token.user_id})
                        return Response({"success": 33,
                                         "post": serializer.data})
                    else:
                        return Response({"error": 34})

                else:
                    return Response({"error": 32})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def remove_comment(request):
    """
Remove comment method.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "comment_id": 1
    }

    Code statuses can be found here: /api/v1/docs/status-code/

    Success json:
    {
        "success": <status_code>,
        "post": {
            "id": 11,
            "author": {
                "id": 2,
                "username": "antonboksha",
                "first_name": "",
                "last_name": "",
                "email": "antonboksha@gmail.com",
                "info": {
                    "full_name": "",
                    "biography": "qweqweqwe",
                    "like_count": 0,
                    "comment_count": 0,
                    "rate": 10,
                    "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                    "is_facebook": false,
                    "is_twitter": false,
                    "is_instagram": false
                },
                "count_downvoted": 1,
                "count_upvoted": 1,
                "count_likes": 1,
                "count_comments": 2,
                "complete_likes": 50
            },
            "text": "here we fucking go!2",
            "like_count": 0,
            "comment_count": 0,
            "date": "2015-11-23T10:44:28.217756Z",
            "permission": true,
            "image": "/media/default_images/default.png",
            "post_hashtags": [
                {
                    "id": 7,
                    "hashtag": "first"
                },
                {
                    "id": 8,
                    "hashtag": "second"
                },
                {
                    "id": 9,
                    "hashtag": "third"
                }
            ],
            "post_comments": [
            {
                "id": 1,
                "text": "Some post text here...",
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 0,
                        "avatar": "/media/default_images/default.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 1,
                    "complete_likes": 50
                },
                "date": "2015-11-23T16:21:24.335014Z",
                "permission": true,
                "rate": 0,
                "is_upvoted": false,
                "is_downvoted": false,
                "best_response": false
            },
            {
                "id": 2,
                "text": "Some post text here...",
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 0,
                        "avatar": "/media/default_images/default.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 1,
                    "complete_likes": 50
                },
                "date": "2015-11-23T16:23:42.295629Z",
                "permission": true,
                "rate": 0,
                "is_upvoted": false,
                "is_downvoted": false,
                "best_response": false
            }],
            "like_count": 0,
            "comment_count": 0
        }
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                if Comment.objects.filter(pk=request.data["comment_id"]).exists():
                    token = get_object_or_404(Token, key=request.data["token"])
                    comment = Comment.objects.get(pk=request.data["comment_id"])
                    if comment.author != token.user_id:
                        return Response({"error": 36})
                    else:
                        comment.delete()
                        post = Post.objects.get(pk=comment.post_id)
                        serializer = PostSerializer(post, context={'user_id': token.user_id})
                        return Response({"success": 37,
                                         "post": serializer.data})
                else:
                    return Response({"error": 35})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def rate_comment(request):
    """
Rate comment method.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "comment_id": 1,
        "statement": true
    }

    Success json:
    {
        "success": 38,
        "post": {
            "id": 11,
            "author": {
                "id": 2,
                "username": "antonboksha",
                "first_name": "",
                "last_name": "",
                "email": "antonboksha@gmail.com",
                "info": {
                    "full_name": "",
                    "biography": "qweqweqwe",
                    "like_count": 0,
                    "comment_count": 0,
                    "rate": 10,
                    "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                    "is_facebook": false,
                    "is_twitter": false,
                    "is_instagram": false
                },
                "count_downvoted": 1,
                "count_upvoted": 1,
                "count_likes": 1,
                "count_comments": 2,
                "complete_likes": 50
            },
            "text": "here we fucking go!2",
            "like_count": 0,
            "comment_count": 0,
            "date": "2015-11-23T10:44:28.217756Z",
            "permission": true,
            "image": "/media/default_images/default.png",
            "post_hashtags": [
                {
                    "id": 7,
                    "hashtag": "first"
                },
                {
                    "id": 8,
                    "hashtag": "second"
                },
                {
                    "id": 9,
                    "hashtag": "third"
                }
            ],
            "post_comments": [
            {
                "id": 1,
                "text": "Some post text here...",
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 0,
                        "avatar": "/media/default_images/default.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 1,
                    "complete_likes": 50
                },
                "date": "2015-11-23T16:21:24.335014Z",
                "permission": true,
                "rate": 0,
                "is_upvoted": false,
                "is_downvoted": false,
                "best_response": false
            },
            {
                "id": 2,
                "text": "Some post text here...",
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 0,
                        "avatar": "/media/default_images/default.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 1,
                    "complete_likes": 50
                },
                "date": "2015-11-23T16:23:42.295629Z",
                "permission": true,
                "rate": 0,
                "is_upvoted": false,
                "is_downvoted": false,
                "best_response": false
            }],
            "like_count": 0,
            "comment_count": 0
        }
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                if Comment.objects.filter(pk=request.data["comment_id"]).exists():
                    token = get_object_or_404(Token, key=request.data["token"])
                    comment = Comment.objects.get(pk=request.data["comment_id"])
                    post = Post.objects.get(pk=comment.post_id)
                    serializer = PostSerializer(post, context={'user_id': token.user_id})
                    if CommentLike.objects.filter(user=token.user_id, comment=comment).exists():
                        like = CommentLike.objects.get(user=token.user_id, comment=comment)
                        if like.statement == request.data["statement"]:
                            return Response({"error": 39,
                                             "post": serializer.data})
                        else:
                            like.statement = request.data["statement"]
                            like.save()
                            if request.data["statement"]:
                                comment.rate += 2
                            else:
                                comment.rate -= 2
                            comment.save()
                    else:
                        CommentLike.objects.create(user_id=token.user_id,
                                                   statement=request.data["statement"],
                                                   comment=comment)
                        if request.data["statement"]:
                            comment.rate += 1
                        else:
                            comment.rate -= 1
                        comment.save()
                    return Response({"success": 38,
                                     "post": serializer.data})
                else:
                    return Response({"error": 35})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def mark_best_response(request):
    """
Mark comment to topic as best response.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "comment_id": 1,
        "best_response": true
    }

    Success json:
    {
        "post": {
            "id": 1,
            "author": {
                "id": 2,
                "username": "antonboksha",
                "first_name": "",
                "last_name": "",
                "email": "antonboksha@gmail.com",
                "info": {
                    "full_name": "",
                    "biography": "qweqweqwe",
                    "like_count": 0,
                    "comment_count": 0,
                    "rate": 10,
                    "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                    "is_facebook": false,
                    "is_twitter": false,
                    "is_instagram": false
                },
                "count_downvoted": 1,
                "count_upvoted": 1,
                "count_likes": 1,
                "count_comments": 2,
                "complete_likes": 50
            },
            "text": "Some post text here...",
            "date": "2015-11-23T16:19:47.570547Z",
            "permission": true,
            "image": "/media/post/4a62f3f2-e4e2-4085-982d-cdb57c0f7ca3.png",
            "post_hashtags": [
                {
                    "id": 1,
                    "hashtag": "first"
                },
                {
                    "id": 2,
                    "hashtag": "second"
                },
                {
                    "id": 3,
                    "hashtag": "third"
                }
            ],
            "post_comments": [
                {
                    "id": 4,
                    "text": "Some post text here...",
                    "author": {
                        "id": 2,
                        "username": "antonboksha",
                        "first_name": "",
                        "last_name": "",
                        "email": "antonboksha@gmail.com",
                        "info": {
                            "full_name": "",
                            "biography": "",
                            "like_count": 0,
                            "comment_count": 0,
                            "rate": 0,
                            "avatar": "/media/default_images/default.png",
                            "is_facebook": false,
                            "is_twitter": false,
                            "is_instagram": false
                        },
                        "count_downvoted": 1,
                        "count_upvoted": 1,
                        "count_likes": 1,
                        "count_comments": 1,
                        "complete_likes": 50
                    },
                    "date": "2015-11-23T16:24:05.060450Z",
                    "permission": true,
                    "rate": -1,
                    "is_upvoted": false,
                    "is_downvoted": true,
                    "best_response": false
                }
            ],
            "like_count": 1,
            "comment_count": 1,
            "is_like": true
        },
        "success": 40
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                if Comment.objects.filter(pk=request.data["comment_id"]).exists():
                    token = get_object_or_404(Token, key=request.data["token"])
                    comment = Comment.objects.get(pk=request.data["comment_id"])
                    post = Post.objects.get(pk=comment.post_id)
                    if post.author_id == token.user_id:
                        comment.best_response = request.data["best_response"]
                        comment.save()
                        serializer = PostSerializer(post, context={'user_id': token.user_id})
                        return Response({"success": 40,
                                         "post": serializer.data})
                    else:
                        return Response({"error": 41})
                else:
                    return Response({"error": 35})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def explore_popular(request):
    """
Explore popular posts.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "offset": 0
    }

    Success json:
    {
        "posts": [
            {
                "id": 1,
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "qweqweqwe",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 10,
                        "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 2,
                    "complete_likes": 50
                },
                "text": "Some post text here...",
                "date": "2015-11-23T16:19:47.570547Z",
                "permission": true,
                "image": "/media/post/4a62f3f2-e4e2-4085-982d-cdb57c0f7ca3.png",
                "post_hashtags": [
                    {
                        "id": 1,
                        "hashtag": "first"
                    },
                    {
                        "id": 2,
                        "hashtag": "second"
                    },
                    {
                        "id": 3,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [
                    {
                        "id": 6,
                        "text": "123",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "qweqweqwe",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2016-02-09T10:00:08.332756Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": true,
                        "is_downvoted": true,
                        "best_response": false
                    }
                ],
                "like_count": 1,
                "comment_count": 1,
                "is_like": true
            },
            {
                "id": 2,
                "text": "Some post text here...",
                "date": "2015-11-23T16:40:39.438305Z",
                "permission": true,
                "image": "/media/post/5f7f8233-7704-4634-b366-6082c3cfbabe.png",
                "post_hashtags": [
                    {
                        "id": 4,
                        "hashtag": "first"
                    },
                    {
                        "id": 5,
                        "hashtag": "second"
                    },
                    {
                        "id": 6,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [],
                "like_count": 0,
                "comment_count": 0,
                "is_like": false
            },
            {
                "id": 3,
                "text": "Some post text here...",
                "date": "2016-02-05T14:02:41.007803Z",
                "permission": true,
                "image": null,
                "post_hashtags": [
                    {
                        "id": 7,
                        "hashtag": "first"
                    },
                    {
                        "id": 8,
                        "hashtag": "second"
                    },
                    {
                        "id": 9,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [],
                "like_count": 0,
                "comment_count": 0,
                "is_like": false
            }
        ],
        "success": 63,
        "offset": 10
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                token = get_object_or_404(Token, key=request.data["token"])
                reported_users = UserReport.objects.filter(user=token.user).values_list('reported_id', flat=True)
                start_offset = request.data["offset"]
                end_offset = start_offset + PAGE_OFFSET
                posts = Post.objects.exclude(author_id__in=reported_users).\
                                     order_by("-count_likes")[start_offset:end_offset]
                serializer = PostSerializer(posts, context={'user_id': token.user_id}, many=True)
                return Response({"success": 63,
                                 "posts": serializer.data,
                                 "offset": end_offset})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def explore_daily_upvotes(request):
    """
Explore daily upvoted comments.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "offset": 0
    }

    Success json:
    {
        "comments": [
            {
                "id": 6,
                "text": "123",
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "qweqweqwe",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 0,
                        "avatar": "/media/default_images/default.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 1,
                    "complete_likes": 50
                },
                "date": "2016-02-09T10:00:08.332756Z",
                "permission": true,
                "rate": 0,
                "is_upvoted": true,
                "is_downvoted": true,
                "best_response": false
            }
        ],
        "success": 64,
        "offset": 40
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                token = get_object_or_404(Token, key=request.data["token"])
                start_time = datetime.datetime.now() - datetime.timedelta(days=1)
                end_time = datetime.datetime.now()
                start_offset = request.data["offset"]
                end_offset = start_offset + PAGE_OFFSET
                comments = Comment.objects.filter(date__range=(start_time, end_time)).\
                                           order_by("-rate")[start_offset:end_offset]
                serializer = PostCommentSerializer(comments, context={'user_id': token.user_id}, many=True)
                return Response({"success": 64,
                                 "comments": serializer.data,
                                 "offset": end_offset})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def explore_most_upvoted(request):
    """
Explore most upvoted comments.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "offset": 10
    }

    Success json:
    {
        "comments": [
            {
                "id": 6,
                "text": "123",
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "qweqweqwe",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 0,
                        "avatar": "/media/default_images/default.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 1,
                    "complete_likes": 50
                },
                "date": "2016-02-09T10:00:08.332756Z",
                "permission": true,
                "rate": 0,
                "is_upvoted": true,
                "is_downvoted": true,
                "best_response": false
            }
        ],
        "success": 65,
        "offset": 50
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                token = get_object_or_404(Token, key=request.data["token"])
                start_offset = request.data["offset"]
                end_offset = start_offset + PAGE_OFFSET
                comments = Comment.objects.all().order_by("-rate")[start_offset:end_offset]
                serializer = PostCommentSerializer(comments, context={'user_id': token.user_id}, many=True)
                return Response({"success": 65,
                                 "comments": serializer.data,
                                 "offset": end_offset})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def search_by_hashtag(request):
    """
Search posts by hashtag.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "hashtag": "test",
        "offset": 0
    }

    Success json:
    {
        "posts": [
            {
                "id": 1,
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "qweqweqwe",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 10,
                        "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 2,
                    "complete_likes": 50
                },
                "text": "Some post text here...",
                "date": "2015-11-23T16:19:47.570547Z",
                "permission": true,
                "image": "/media/post/4a62f3f2-e4e2-4085-982d-cdb57c0f7ca3.png",
                "post_hashtags": [
                    {
                        "id": 1,
                        "hashtag": "first"
                    },
                    {
                        "id": 2,
                        "hashtag": "second"
                    },
                    {
                        "id": 3,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [
                    {
                        "id": 6,
                        "text": "123",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "qweqweqwe",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2016-02-09T10:00:08.332756Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": true,
                        "is_downvoted": true,
                        "best_response": false
                    }
                ],
                "like_count": 1,
                "comment_count": 1,
                "is_like": true
            },
            {
                "id": 2,
                "text": "Some post text here...",
                "date": "2015-11-23T16:40:39.438305Z",
                "permission": true,
                "image": "/media/post/5f7f8233-7704-4634-b366-6082c3cfbabe.png",
                "post_hashtags": [
                    {
                        "id": 4,
                        "hashtag": "first"
                    },
                    {
                        "id": 5,
                        "hashtag": "second"
                    },
                    {
                        "id": 6,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [],
                "like_count": 0,
                "comment_count": 0,
                "is_like": false
            },
            {
                "id": 3,
                "text": "Some post text here...",
                "date": "2016-02-05T14:02:41.007803Z",
                "permission": true,
                "image": null,
                "post_hashtags": [
                    {
                        "id": 7,
                        "hashtag": "first"
                    },
                    {
                        "id": 8,
                        "hashtag": "second"
                    },
                    {
                        "id": 9,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [],
                "like_count": 0,
                "comment_count": 0,
                "is_like": false
            }
        ],
        "success": 66,
        "offset": 70
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                token = get_object_or_404(Token, key=request.data["token"])
                posts_ids = PostHashtag.objects.filter(hashtag=request.data["hashtag"]).\
                    values_list("post_id", flat=True)
                start_offset = request.data["offset"]
                end_offset = start_offset + PAGE_OFFSET
                posts = Post.objects.filter(pk__in=posts_ids)[start_offset:end_offset]
                serializer = PostSerializer(posts, context={'user_id': token.user_id}, many=True)
                return Response({"success": 66,
                                 "posts": serializer.data,
                                 "offset": end_offset})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def explore_popular_search(request):
    """
Search explore popular posts.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "keyword": "qwerty",
        "offset": 0
    }

    Success json:
    {
        "posts": [
            {
                "id": 1,
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "qweqweqwe",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 10,
                        "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 2,
                    "complete_likes": 50
                },
                "text": "Some post text here...",
                "date": "2015-11-23T16:19:47.570547Z",
                "permission": true,
                "image": "/media/post/4a62f3f2-e4e2-4085-982d-cdb57c0f7ca3.png",
                "post_hashtags": [
                    {
                        "id": 1,
                        "hashtag": "first"
                    },
                    {
                        "id": 2,
                        "hashtag": "second"
                    },
                    {
                        "id": 3,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [
                    {
                        "id": 6,
                        "text": "123",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "qweqweqwe",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2016-02-09T10:00:08.332756Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": true,
                        "is_downvoted": true,
                        "best_response": false
                    }
                ],
                "like_count": 1,
                "comment_count": 1,
                "is_like": true
            },
            {
                "id": 2,
                "text": "Some post text here...",
                "date": "2015-11-23T16:40:39.438305Z",
                "permission": true,
                "image": "/media/post/5f7f8233-7704-4634-b366-6082c3cfbabe.png",
                "post_hashtags": [
                    {
                        "id": 4,
                        "hashtag": "first"
                    },
                    {
                        "id": 5,
                        "hashtag": "second"
                    },
                    {
                        "id": 6,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [],
                "like_count": 0,
                "comment_count": 0,
                "is_like": false
            },
            {
                "id": 3,
                "text": "Some post text here...",
                "date": "2016-02-05T14:02:41.007803Z",
                "permission": true,
                "image": null,
                "post_hashtags": [
                    {
                        "id": 7,
                        "hashtag": "first"
                    },
                    {
                        "id": 8,
                        "hashtag": "second"
                    },
                    {
                        "id": 9,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [],
                "like_count": 0,
                "comment_count": 0,
                "is_like": false
            }
        ],
        "success": 63,
        "offset": 10
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                token = get_object_or_404(Token, key=request.data["token"])
                start_offset = request.data["offset"]
                end_offset = start_offset + PAGE_OFFSET
                posts = Post.objects.filter(text__contains=request.data["keyword"]).\
                                     order_by("-count_likes")[start_offset:end_offset]
                serializer = PostSerializer(posts, context={'user_id': token.user_id}, many=True)
                return Response({"success": 63,
                                 "posts": serializer.data,
                                 "offset": end_offset})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def explore_daily_upvotes_search(request):
    """
Search explore daily upvoted comments.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "keyword": "qwerty",
        "offset": 10
    }

    Success json:
    {
        "comments": [
            {
                "id": 6,
                "text": "123",
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "qweqweqwe",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 0,
                        "avatar": "/media/default_images/default.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 1,
                    "complete_likes": 50
                },
                "date": "2016-02-09T10:00:08.332756Z",
                "permission": true,
                "rate": 0,
                "is_upvoted": true,
                "is_downvoted": true,
                "best_response": false
            }
        ],
        "success": 64,
        "offset": 20
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                token = get_object_or_404(Token, key=request.data["token"])
                start_time = datetime.datetime.now() - datetime.timedelta(days=1)
                end_time = datetime.datetime.now()
                start_offset = request.data["offset"]
                end_offset = start_offset + PAGE_OFFSET
                comments = Comment.objects.filter(date__range=(start_time, end_time),
                                                  text__contains=request.data["keyword"]).\
                                           order_by("-rate")[start_offset: end_offset]
                serializer = PostCommentSerializer(comments, context={'user_id': token.user_id}, many=True)
                return Response({"success": 64,
                                 "comments": serializer.data,
                                 "offset": end_offset})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def explore_most_upvoted_search(request):
    """
Search explore most upvoted comments.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "keyword": "qwerty",
        "offset": 10
    }

    Success json:
    {
        "comments": [
            {
                "id": 6,
                "text": "123",
                "author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "qweqweqwe",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 0,
                        "avatar": "/media/default_images/default.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 1,
                    "complete_likes": 50
                },
                "date": "2016-02-09T10:00:08.332756Z",
                "permission": true,
                "rate": 0,
                "is_upvoted": true,
                "is_downvoted": true,
                "best_response": false
            }
        ],
        "success": 65,
        "offset": 20
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                token = get_object_or_404(Token, key=request.data["token"])
                start_offset = request.data["offset"]
                end_offset = start_offset + PAGE_OFFSET
                comments = Comment.objects.filter(text__contains=request.data["keyword"]).\
                                           order_by("-rate")[start_offset:end_offset]
                serializer = PostCommentSerializer(comments, context={'user_id': token.user_id}, many=True)
                return Response({"success": 65,
                                 "comments": serializer.data,
                                 "offset": end_offset})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def get_single_post(request):
    """
Get single post method.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "post_id": 0
    }

    Code statuses can be found here: /api/v1/docs/status-code/

    Success json:
    {
        "post": {
            "id": 1,
            "author": {
                "id": 2,
                "username": "antonboksha1",
                "first_name": "",
                "last_name": "",
                "email": "antonboksha1@gmail.com",
                "info": {
                    "full_name": "",
                    "biography": "qweqweqwe",
                    "like_count": 0,
                    "comment_count": 0,
                    "rate": 7,
                    "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                    "is_facebook": true,
                    "is_twitter": true,
                    "is_instagram": false,
                    "facebook_url": "https://www.facebook.com/app_scoped_user_id/1168737826510483",
                    "twitter_url": "https://twitter.com/durov",
                    "instagram_url": ""
                },
                "count_downvoted": 1,
                "count_upvoted": 1,
                "count_likes": 1,
                "count_comments": 6,
                "complete_likes": 50
            },
            "text": "Some post text here...",
            "date": "16:19:47 2015:11:23",
            "permission": true,
            "image": "/media/post/4a62f3f2-e4e2-4085-982d-cdb57c0f7ca3.png",
            "post_hashtags": [
                {
                    "id": 1,
                    "hashtag": "first"
                },
                {
                    "id": 2,
                    "hashtag": "second"
                },
                {
                    "id": 3,
                    "hashtag": "third"
                }
            ],
            "post_comments": [
                {
                    "id": 6,
                    "text": "123",
                    "author": {
                        "id": 2,
                        "username": "antonboksha1",
                        "first_name": "",
                        "last_name": "",
                        "email": "antonboksha1@gmail.com",
                        "info": {
                            "full_name": "",
                            "biography": "qweqweqwe",
                            "like_count": 0,
                            "comment_count": 0,
                            "rate": 7,
                            "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                            "is_facebook": true,
                            "is_twitter": true,
                            "is_instagram": false,
                            "facebook_url": "https://www.facebook.com/app_scoped_user_id/1168737826510483",
                            "twitter_url": "https://twitter.com/durov",
                            "instagram_url": ""
                        },
                        "count_downvoted": 1,
                        "count_upvoted": 1,
                        "count_likes": 1,
                        "count_comments": 6,
                        "complete_likes": 50
                    },
                    "date": "10:00:08 2016:02:09",
                    "permission": true,
                    "rate": 0,
                    "is_upvoted": false,
                    "is_downvoted": false,
                    "best_response": false
                },
                {
                    "id": 7,
                    "text": "jkh",
                    "author": {
                        "id": 2,
                        "username": "antonboksha1",
                        "first_name": "",
                        "last_name": "",
                        "email": "antonboksha1@gmail.com",
                        "info": {
                            "full_name": "",
                            "biography": "qweqweqwe",
                            "like_count": 0,
                            "comment_count": 0,
                            "rate": 7,
                            "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                            "is_facebook": true,
                            "is_twitter": true,
                            "is_instagram": false,
                            "facebook_url": "https://www.facebook.com/app_scoped_user_id/1168737826510483",
                            "twitter_url": "https://twitter.com/durov",
                            "instagram_url": ""
                        },
                        "count_downvoted": 1,
                        "count_upvoted": 1,
                        "count_likes": 1,
                        "count_comments": 6,
                        "complete_likes": 50
                    },
                    "date": "13:26:43 2016:02:22",
                    "permission": true,
                    "rate": 4,
                    "is_upvoted": false,
                    "is_downvoted": false,
                    "best_response": false
                },
                {
                    "id": 8,
                    "text": "dsfdssdfsdff..",
                    "author": {
                        "id": 2,
                        "username": "antonboksha1",
                        "first_name": "",
                        "last_name": "",
                        "email": "antonboksha1@gmail.com",
                        "info": {
                            "full_name": "",
                            "biography": "qweqweqwe",
                            "like_count": 0,
                            "comment_count": 0,
                            "rate": 7,
                            "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                            "is_facebook": true,
                            "is_twitter": true,
                            "is_instagram": false,
                            "facebook_url": "https://www.facebook.com/app_scoped_user_id/1168737826510483",
                            "twitter_url": "https://twitter.com/durov",
                            "instagram_url": ""
                        },
                        "count_downvoted": 1,
                        "count_upvoted": 1,
                        "count_likes": 1,
                        "count_comments": 6,
                        "complete_likes": 50
                    },
                    "date": "16:39:12 2016:04:02",
                    "permission": true,
                    "rate": 0,
                    "is_upvoted": false,
                    "is_downvoted": false,
                    "best_response": false
                },
                {
                    "id": 9,
                    "text": "dsfdssdfsdff..",
                    "author": {
                        "id": 2,
                        "username": "antonboksha1",
                        "first_name": "",
                        "last_name": "",
                        "email": "antonboksha1@gmail.com",
                        "info": {
                            "full_name": "",
                            "biography": "qweqweqwe",
                            "like_count": 0,
                            "comment_count": 0,
                            "rate": 7,
                            "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                            "is_facebook": true,
                            "is_twitter": true,
                            "is_instagram": false,
                            "facebook_url": "https://www.facebook.com/app_scoped_user_id/1168737826510483",
                            "twitter_url": "https://twitter.com/durov",
                            "instagram_url": ""
                        },
                        "count_downvoted": 1,
                        "count_upvoted": 1,
                        "count_likes": 1,
                        "count_comments": 6,
                        "complete_likes": 50
                    },
                    "date": "16:39:39 2016:04:02",
                    "permission": true,
                    "rate": 0,
                    "is_upvoted": false,
                    "is_downvoted": false,
                    "best_response": false
                },
                {
                    "id": 10,
                    "text": "dsfdssdfs123123dff..",
                    "author": {
                        "id": 2,
                        "username": "antonboksha1",
                        "first_name": "",
                        "last_name": "",
                        "email": "antonboksha1@gmail.com",
                        "info": {
                            "full_name": "",
                            "biography": "qweqweqwe",
                            "like_count": 0,
                            "comment_count": 0,
                            "rate": 7,
                            "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                            "is_facebook": true,
                            "is_twitter": true,
                            "is_instagram": false,
                            "facebook_url": "https://www.facebook.com/app_scoped_user_id/1168737826510483",
                            "twitter_url": "https://twitter.com/durov",
                            "instagram_url": ""
                        },
                        "count_downvoted": 1,
                        "count_upvoted": 1,
                        "count_likes": 1,
                        "count_comments": 6,
                        "complete_likes": 50
                    },
                    "date": "16:39:44 2016:04:02",
                    "permission": true,
                    "rate": 0,
                    "is_upvoted": false,
                    "is_downvoted": false,
                    "best_response": false
                },
                {
                    "id": 11,
                    "text": "dsfdssdfs12312222223dff..",
                    "author": {
                        "id": 2,
                        "username": "antonboksha1",
                        "first_name": "",
                        "last_name": "",
                        "email": "antonboksha1@gmail.com",
                        "info": {
                            "full_name": "",
                            "biography": "qweqweqwe",
                            "like_count": 0,
                            "comment_count": 0,
                            "rate": 7,
                            "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                            "is_facebook": true,
                            "is_twitter": true,
                            "is_instagram": false,
                            "facebook_url": "https://www.facebook.com/app_scoped_user_id/1168737826510483",
                            "twitter_url": "https://twitter.com/durov",
                            "instagram_url": ""
                        },
                        "count_downvoted": 1,
                        "count_upvoted": 1,
                        "count_likes": 1,
                        "count_comments": 6,
                        "complete_likes": 50
                    },
                    "date": "16:40:05 2016:04:02",
                    "permission": true,
                    "rate": 0,
                    "is_upvoted": false,
                    "is_downvoted": false,
                    "best_response": false
                }
            ],
            "like_count": 1,
            "comment_count": 6,
            "is_like": false
        },
        "success": 87
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                if Post.objects.filter(pk=request.data["post_id"]).exists():
                    token = get_object_or_404(Token, key=request.data["token"])
                    post = Post.objects.get(pk=request.data["post_id"])
                    serializer = PostSerializer(post, context={'user_id': token.user_id})
                    return Response({"success": 87,
                                     "post": serializer.data})
                else:
                    return Response({"error": 88})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def remove_post(request):
    """
Remove post by id.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "post_id": 12
    }

    Code statuses can be found here: /api/v1/docs/status-code/

    Success json:
    {
        "success": True
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                if Post.objects.filter(pk=request.data["post_id"]).exists():
                    Post.objects.get(pk=request.data["post_id"]).delete()
                    return Response({"success": 91})
                else:
                    return Response({"error": 32})
            else:
                return Response({"error": 17})


@api_view(["POST"])
def get_user_new_posts(request):
    """
Get user all posts method.

    Example json:
    {
        "token": "9bb7176dcdd06d196ef38c17600840d13943b9df",
        "latest_id": 123
    }

    Code statuses can be found here: /api/v1/docs/status-code/

    Success json:
    {
        "post": [
            {
                "id": 1,
                author": {
                    "id": 2,
                    "username": "antonboksha",
                    "first_name": "",
                    "last_name": "",
                    "email": "antonboksha@gmail.com",
                    "info": {
                        "full_name": "",
                        "biography": "qweqweqwe",
                        "like_count": 0,
                        "comment_count": 0,
                        "rate": 10,
                        "avatar": "/media/userprofile/849d5d9c-e968-4c7c-b96c-23aa46a719fd.png",
                        "is_facebook": false,
                        "is_twitter": false,
                        "is_instagram": false
                    },
                    "count_downvoted": 1,
                    "count_upvoted": 1,
                    "count_likes": 1,
                    "count_comments": 2,
                    "complete_likes": 50
                },
                "text": "Some post text here...",
                "like_count": 0,
                "comment_count": 0,
                "date": "2015-11-23T16:19:47.570547Z",
                "permission": true,
                "image": "/media/post/4a62f3f2-e4e2-4085-982d-cdb57c0f7ca3.png",
                "post_hashtags": [
                    {
                        "id": 1,
                        "hashtag": "first"
                    },
                    {
                        "id": 2,
                        "hashtag": "second"
                    },
                    {
                        "id": 3,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [
                    {
                        "id": 1,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:21:24.335014Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    },
                    {
                        "id": 2,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:23:42.295629Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    },
                    {
                        "id": 3,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:24:03.634480Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    },
                    {
                        "id": 4,
                        "text": "Some post text here...",
                        "author": {
                            "id": 2,
                            "username": "antonboksha",
                            "first_name": "",
                            "last_name": "",
                            "email": "antonboksha@gmail.com",
                            "info": {
                                "full_name": "",
                                "biography": "",
                                "like_count": 0,
                                "comment_count": 0,
                                "rate": 0,
                                "avatar": "/media/default_images/default.png",
                                "is_facebook": false,
                                "is_twitter": false,
                                "is_instagram": false
                            },
                            "count_downvoted": 1,
                            "count_upvoted": 1,
                            "count_likes": 1,
                            "count_comments": 1,
                            "complete_likes": 50
                        },
                        "date": "2015-11-23T16:24:05.060450Z",
                        "permission": true,
                        "rate": 0,
                        "is_upvoted": false,
                        "is_downvoted": false,
                        "best_response": false
                    }
                ],
                "like_count": 0,
                "comment_count": 0
            },
            {
                "id": 2,
                "text": "Some post text here...",
                "like_count": 0,
                "comment_count": 0,
                "date": "2015-11-23T16:40:39.438305Z",
                "permission": true,
                "image": "/media/post/5f7f8233-7704-4634-b366-6082c3cfbabe.png",
                "post_hashtags": [
                    {
                        "id": 4,
                        "hashtag": "first"
                    },
                    {
                        "id": 5,
                        "hashtag": "second"
                    },
                    {
                        "id": 6,
                        "hashtag": "third"
                    }
                ],
                "post_comments": [],
                "like_count": 0,
                "comment_count": 0
            }
        ],
        "success": 29,
    }

    Fail json:
    {
        "error": <status_code>
    }
    """
    if request.method == "POST":
        if "token" in request.data and request.data["token"] != "" and request.data["token"] is not None:
            if Token.objects.filter(key=request.data["token"]).exists():
                token = get_object_or_404(Token, key=request.data["token"])
                posts = Post.objects.filter(pk__gt=request.data["latest_id"]).order_by("-date")[:PAGE_OFFSET]
                serializer = PostSerializer(posts, many=True, context={'user_id': token.user_id})
                return Response({"success": 29,
                                 "post": serializer.data})
            else:
                return Response({"error": 17})
