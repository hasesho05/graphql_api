import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from .models import User, Post
import graphql_jwt


class PostType(DjangoObjectType):
    class Meta:
        model = Post

    post_new = graphene.String()

    def resolve_post_new(self, info):
        return "Old Post" if self.publish < 1999 else "New Post"


class UserType(DjangoObjectType):
    class Meta:
        model = User


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = {
            "channel_name": ["exact", "icontains", "istartswith"],
            "caption": ["exact", "icontains"],
            "video_url": ["exact", "icontains"],
            "music_name": ["exact", "icontains"],
        }
        interfaces = (relay.Node,)


class PostUpdateMutationRelay(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        channel_name = graphene.String()
        caption = graphene.String()
        video_url = graphene.String()
        music_name = graphene.String()

    post = graphene.Field(PostNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, **input):
        post = Post.objects.get(pk=id)
        post.channel_name = input.get("channel_name")
        post.caption = input.get("caption")
        post.video_url = input.get("video_url")
        post.music_name = input.get("music_name")
        post.save()

        return PostUpdateMutationRelay(post=post)


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int(), channel_name=graphene.String())

    def resolve_post(self, info, **kwargs):
        id = kwargs.get("id")
        channel_name = kwargs.get("channel_name")

        if id is not None:
            return Post.objects.get(pk=id)

        if channel_name is not None:
            return Post.objects.get(channel_name=channel_name)

        return None

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.order_by("-created_at")


class PostCreateMutation(graphene.Mutation):
    class Arguments:
        channel_name = graphene.String()
        caption = graphene.String()
        video_url = graphene.String()
        music_name = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, channel_name, caption, video_url, music_name):
        post = Post(channel_name=channel_name, caption=caption, video_url=video_url, music_name=music_name)
        post.save()

        return PostCreateMutation(post=post)


class PostUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        channel_name = graphene.String()
        caption = graphene.String()
        video_url = graphene.String()
        music_name = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, id, channel_name, caption, video_url, music_name):
        post = Post.objects.get(pk=id)
        post.channel_name = channel_name
        post.caption = caption
        post.video_url = video_url
        post.music_name = music_name
        post.save()

        return PostUpdateMutation(post=post)


class PostDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, id):
        post = Post.objects.get(pk=id)
        post.delete()

        return PostDeleteMutation(post=post)


class Mutation:
    post_create = PostCreateMutation.Field()
    post_update = PostUpdateMutation.Field()
    post_delete = PostDeleteMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
