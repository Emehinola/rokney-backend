from users_account.models import CustomUser
import graphene
from graphql_auth import mutations
from graphene_django import DjangoObjectType, DjangoListField
from graphene_file_upload.scalars import Upload
from . models import Comment, Post, FileAlbum, Like
from users_account.schema import UserType
import datetime

""" DEFINING OBJECT TYPES """


class PostType(DjangoObjectType):  # for posts
    class Meta:
        model = Post


class FileAlbumType(DjangoObjectType):  # for file albums
    class Meta:
        model = FileAlbum


class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class CommentType(DjangoObjectType):  # for comment type
    class Meta:
        model = Comment


""" DEFINING INPUTS """


class PostInput(graphene.InputObjectType):
    user_email = graphene.String(required=True)
    content = graphene.String()
    images = graphene.List(Upload)
    date_time = graphene.DateTime()
    subtitle = graphene.String()


class CommentInput(graphene.InputObjectType):
    content = graphene.String()
    post_id = graphene.Int()
    email = graphene.String()
    time = graphene.DateTime()


class LikeInput(graphene.InputObjectType):
    post_id = graphene.Int()
    user_email = graphene.String()


""" MUTATIONS """


class CreatePost(graphene.Mutation):
    class Arguments:
        post = PostInput()

    success = graphene.Boolean()
    error = graphene.String()

    @staticmethod
    def mutate(parent, info, post):
        try:
            user_email = post.user_email
            user = CustomUser.objects.get(email=user_email)
            create_post = Post(
                user=user,
                content=post.content,
                subtitle=post.subtitle,
                time=datetime.datetime.now()
            )

            create_post.save()

            # creating album for post

            for image in post.images:
                FileAlbum(
                    post=create_post,
                    images=image
                ).save()

            return CreatePost(success=True, error=None)

        except CustomUser.DoesNotExist:
            CreatePost(success=False, error="No such user in the database")


class CreateComment(graphene.Mutation):
    class Arguments:
        comment = CommentInput()

    success = graphene.Boolean()
    error = graphene.String()

    @staticmethod
    def mutate(parent, info, comment):
        try:
            user = CustomUser.objects.get(email=comment.email)
            post = Post.objects.get(id=comment.post_id)

            if comment.content is not None:
                content = Comment(
                    content=comment.content,
                    post=post,
                    time=comment.time,
                    user=user
                )
                content.save()  # saves comment to the database
                return CreateComment(success=True, error=None)

            return CreateComment(success=False, error="Comment can't be empty")

        except:
            return CreateComment(success=False, error="Comment not created")

# creating post likes


class CreateLike(graphene.Mutation):
    class Arguments:
        like = LikeInput()

    success = graphene.Boolean()
    error = graphene.String()
    message = graphene.String()

    @staticmethod
    def mutate(parent, info, like):
        try:
            post = Post.objects.get(id=like.post_id)
            user = CustomUser.objects.get(email=like.user_email)

            # checks if the post has already been liked by that user
            if Like.objects.filter(user=user, post=post).exists():
                # unlikes the post if it has already been liked by the user
                Like.objects.get(user=user, post=post).delete()
                return CreateLike(success=True, error=None, message="post unliked")

            # creating like model
            likeModel = Like(
                user=user,
                post=post
            )
            likeModel.save()

            return CreateLike(success=True, error=None, message="post liked")

        except (Post.DoesNotExist or CustomUser.DoesNotExist):
            return CreateLike(success=False, error="Either the user or post does not exist", message="error")


""" QUERYING """


class QueryPost(graphene.ObjectType):
    posts = DjangoListField(PostType)
    get_post = graphene.Field(PostType, post_id=graphene.Int())
    get_post_search = DjangoListField(
        PostType, keyword=graphene.String())  # for getting searches
    posts = DjangoListField(PostType)

    # getting posts

    @staticmethod
    def resolve_posts(parent, info, **kwargs):
        return Post.objects.all()  # returns all posts

    @staticmethod
    def resolve_get_post(parent, info, post_id):
        # gets a post by it's id
        return Post.objects.get(id=post_id)

    @staticmethod
    def resolve_get_post_search(parent, info, keyword):
        # searches for posts with the entered keyword
        return Post.objects.filter(content__icontains=keyword)


class QueryFileAlbum(graphene.ObjectType):
    albums = DjangoListField(FileAlbumType)

    @staticmethod
    def resolve_albums(parent, info, **kwargs):
        return FileAlbum.objects.all()


class QueryPostLike(graphene.ObjectType):
    likes = DjangoListField(LikeType)

    @staticmethod
    def resolve_likes(parent, info, likes):
        return Like.objects.all()


class QueryComment(graphene.ObjectType):
    comments = DjangoListField(CommentType, post_id=graphene.Int())

    @staticmethod
    def resolve_comments(parent, info, post_id):
        try:
            # gets the post associated with the comment
            post = Post.objects.get(id=post_id)
            comments = Comment.objects.filter(post=post)
            return comments

        except Post.DoesNotExist:
            return None
