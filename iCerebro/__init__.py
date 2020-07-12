from time import sleep
from typing import List

from instapy import InstaPy
from iCerebro.database import IgDb, User
from iCerebro.db_utils import scrap_for_user_relationships, store_all_posts_of_user
from iCerebro.image_analisis import ImageAnalysis
from iCerebro.natural_flow import like_by_tags, follow_user_follow, like_by_users
from iCerebro.upload import upload_single_image


class ICerebro(InstaPy):

    def __init__(
            self,
            *args,
            **kwargs,
    ):
        super(self.__class__, self).__init__(*args, **kwargs)

        self.use_image_analysis = False
        self.ImgAn = None
        self.store_in_database = False
        self.db = None

    def set_use_image_analysis(
            self,
            use_image_analysis: bool,
            classification_model_name: str = 'resnext101_32x8d',
            detection_model_name: str = 'fasterrcnn_resnet50_fpn',
    ):
        self.use_image_analysis = use_image_analysis
        if use_image_analysis:
            self.ImgAn = ImageAnalysis(
                classification_model_name, detection_model_name)
        else:
            self.ImgAn = None

    def set_store_in_database(
            self,
            store_in_database: bool
    ):
        self.store_in_database = store_in_database
        if store_in_database:
            self.db = IgDb()
        else:
            self.db = None

    def nf_like_by_tags(
            self,
            tags: List[str] = None,
            amount: int = 50,
            skip_top_posts: bool = True,
            use_smart_hashtags: bool = False,
            use_smart_location_hashtags: bool = False,
    ):
        like_by_tags(self, tags, amount, skip_top_posts, use_smart_hashtags, use_smart_location_hashtags)

    def nf_like_by_users(
        self,
        usernames: List[str],
        amount: int = None,
        users_validated: bool = False
    ):
        like_by_users(self, usernames, amount, users_validated)

    def nf_follow_user_follow(
            self,
            follow: str,
            usernames: List[str],
            amount: int = 10,
            randomize: bool = False
    ):
        follow_user_follow(self, follow, usernames, amount, randomize)

    def nf_upload_single_image(self, image_name: str, text: str, insta_username: str):
        upload_single_image(self, image_name, text, insta_username)

    def complete_user_relationships_of_users_already_in_db(self):
        for user in self.db.session.query(User).yield_per(100).enable_eagerloads(False):
            scrap_for_user_relationships(self, user.username)
            sleep(15)

    def complete_posts_of_users_already_in_db(self):
        for user in self.db.session.query(User).yield_per(100).enable_eagerloads(False):
            store_all_posts_of_user(self, user.username)
            sleep(15)