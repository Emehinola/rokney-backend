from django.db.models import fields
import graphene
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import graphql_jwt
from graphene_django import DjangoObjectType, DjangoListField
from users_account.models import Profile, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from graphene_file_upload.scalars import Upload
from users_account.schema import *

# importing from post app schema.py
from post.schema import *


class Query(UserQuery, ProfileQuery, MeQuery, LogoutQuery, QueryUser, QueryPost, QueryFileAlbum, QueryComment, graphene.ObjectType):
    # me = graphene.Field(MeQuery)

    # def resolve_me(self, info):
    #     return info.context.user
    pass


class ObjectMutation(graphene.ObjectType):
    # registers a user with the passed arguments
    register = mutations.Register.Field()

    verify_account = mutations.VerifyAccount.Field()  # for verifying created accounts

    token_auth = mutations.ObtainJSONWebToken.Field()  # for authenticating the user
    verify_token = graphql_jwt.Verify.Field()  # verifies the returned token
    refresh_token = graphql_jwt.Refresh.Field()  # refereshes the token

    # for profile mutation
    create_profile = ProfileCreation.Field()  # for profile creation
    login = Login.Field()  # for login request
    update_profile = ProfileUpdateMutation.Field()  # for profile update

    # for post related
    create_comment = CreateComment.Field()  # for comment to post
    # for creating post likes -> CreateLike() imported from post.schema
    create_like = CreateLike.Field()
    create_post = CreatePost.Field()


class Mutation(ObjectMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
