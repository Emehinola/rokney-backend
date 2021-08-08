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


""" TYPES GO HERE """


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile  # model to affect


class UserType(DjangoObjectType, MeQuery):
    class Meta:
        model = CustomUser


""" INPUTS GO HERE """


class ProfileInput(graphene.InputObjectType):
    user_email = graphene.String(required=True)
    username = graphene.String()
    profile_pic = Upload()
    bio = graphene.String(required=False)
    about = graphene.String(required=False)
    address = graphene.String()
    professions = graphene.String()
    verified_user = graphene.Boolean(default=False)
    followers = graphene.Int()
    following = graphene.Int()

# PROFILE UPDATE INPUTS


class ProfileUpdateInput(graphene.InputObjectType):
    # for getting the profile to update by it's email
    profile = graphene.Field(ProfileInput)

# LOGIN INPUTS


class LoginInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)


""" MUTATIONS GO HERE """


class ProfileCreation(graphene.Mutation):
    class Arguments:
        profile_input = ProfileInput()

    # outputs
    # returns true if profile is created successfully, otherwise false
    success = graphene.Boolean()
    errors = graphene.String()  # errors returned, returns null if there is no error

    @staticmethod
    def mutate(self, info, profile_input):
        try:  # tries to make sure the user with the specified id is in the database
            user = CustomUser.objects.get(email=profile_input.user_email)

            try:  # checks if the profile already exists
                Profile.objects.get(user=user)
                error = "Profile already created for this user"
                return ProfileCreation(success=False, errors=error)

            except Profile.DoesNotExist:  # if there is exception, then it creates the profile for the user
                Profile(
                    user=user,
                    bio=profile_input.bio,
                    about=profile_input.about,
                    followers=profile_input.followers,
                    following=profile_input.following
                ).save()  # creates the save a user profile with the entered values

                return ProfileCreation(success=True, errors=None)

        except CustomUser.DoesNotExist:
            error = "User with email: {} not found".format(profile_input.email)
            return ProfileCreation(success=False, errors=error)

# PROFILE UPDATE MUTATION


class ProfileUpdateMutation(graphene.Mutation):
    """ FOR CAUSING UPDATE TO THE DATABASE """
    class Arguments:
        """ FOR RECEIVING INPUTS """
        profile_update_input = ProfileInput()  # has all the fields required by user

    # returned results
    success = graphene.Boolean()
    image_url = graphene.String()
    error = graphene.String()
    profile = graphene.Field(ProfileType)

    # ccausing mutation, i.e change
    @staticmethod
    def mutate(self, info, profile_update_input):
        try:
            # gets user associated with the email
            user = CustomUser.objects.get(
                email=profile_update_input.user_email)

            # gets the profile associated with the user
            previous_profile = Profile.objects.get(user=user)
            profile_input = profile_update_input

            # checking if the username is already taken by someone else
            # returns true if username already exists apart from the one being used by the user currently
            if profile_input.username != None:
                if CustomUser.objects.filter(username=profile_input.username.lower()).exclude(username=user.username).exists():
                    return ProfileUpdateMutation(profile=None, success=False, error="Username already taken by another user")

            # updating profile with the entered data, if not None
            user.username = profile_input.username if profile_input.username != None else user.username
            previous_profile.profile_pic = profile_input.profile_pic if profile_input.profile_pic != None else previous_profile.profile_pic
            previous_profile.bio = profile_input.bio if profile_input.bio != None else previous_profile.bio
            previous_profile.about = profile_input.about if profile_input.about != None else previous_profile.about
            previous_profile.professions = profile_input.professions if profile_input.professions != None else previous_profile.professions
            previous_profile.address = profile_input.address if profile_input.address != None else previous_profile.address

            # saving changes made to the previous profile
            previous_profile.save()
            user.save()  # saves change to username

            # setting image url
            url = previous_profile.profile_pic.url

            return ProfileUpdateMutation(profile=previous_profile, success=True, error=None, image_url=url)

        except CustomUser.DoesNotExist:
            return ProfileUpdateMutation(profile=None, success=False,
                                         error="No such user on the database")

# LOGIN MUTATION; FOR LOGGING IN AUTHENTICATED USER


class Login(graphene.Mutation):
    class Arguments:
        # inputs for authentication: username and password
        user_data = LoginInput()

    # returned values
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.String()

    # declaring mutation method
    @staticmethod
    def mutate(self, info, user_data):
        user = authenticate(username=user_data.username,
                            password=user_data.password)

        if user:  # returns True if user is authentiicated, otherwise False
            request = info.context
            authenticated_user = CustomUser.objects.get(
                Q(username=user_data.username) | Q(email=user_data.username))  # gets the logged in user

            login(request, user)  # logs the authenticated user in

            return Login(user=authenticated_user, success=True, errors=None)

        return Login(success=False, errors="Incorrect password or username/email")


""" COMBINE ALL MUTATIONS """


""" QUERIES GO HERE """


class ProfileQuery(graphene.ObjectType):
    profiles = DjangoListField(ProfileType)  # returns profile
    profile_by_email = graphene.Field(
        ProfileType, user_email=graphene.String())  # takes user_email as input and returns profile with that email

    @staticmethod
    def resolve_profiles(self, info, **kwargs):
        return Profile.objects.all()  # returns all profile objects in the database

    @staticmethod
    def resolve_profile_by_email(self, info, user_email):
        try:  # try to avoid exception by checking if a profile exists for the queried user
            user = CustomUser.objects.get(email=user_email)
            profile = Profile.objects.get(user=user)

            return profile

        except Profile.DoesNotExist:
            profile = None
            return profile


# LOGOUT QUERY


class LogoutQuery(graphene.ObjectType):
    logout = graphene.Boolean()

    @staticmethod
    def resolve_logout(self, info, **kwargs):
        logout(info.context)  # logs out the currently logged in user

        return True


class QueryUser(graphene.ObjectType):
    get_user = graphene.Field(UserType, email=graphene.String(required=True))

    @staticmethod
    def resolve_get_user(self, info, email):  # gets user by email
        try:
            user = CustomUser.objects.get(email=email)
            return user

        except CustomUser.DoesNotExist:
            return None
