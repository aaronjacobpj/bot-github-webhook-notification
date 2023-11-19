import json
import os

import requests


class GoogleSpace:
    """
    A class for Manging sending github event to Google space.

    Attributes:
        bot (str): The name of the bot.
        bot_subtitle (str): Subtitle for the bot.
        bot_image (str): Url endpoint for bot's avatar
        bot_alt_image_text (str): Alt text fot the bot's avata image.
        file_text_color (str): Color code for filename in the message (Hexadecimal)
        commit_button_color (list[float]): Color code for the link to github commit page
        commit_branch_color (str): Color code for branch name text
    """

    def __init__(
        self,
        bot="Daisy",
        bot_subtitle="Github Bot - Daisy",
        bot_image="https://developers.google.com/chat/images/quickstart-app-avatar.png",
        bot_alt_image_text="Avatar for Daisy",
        file_text_color="#e11d48",
        commit_button_color=[0.4, 0.8, 0.77, 0.5],
        commit_branch_color="#0766AD",
    ) -> None:
        """
        Initializes an Employee object.

        Parameters:
            bot (str): The name of the bot.
            bot_subtitle (str): Subtitle for the bot.
            bot_image (str): Url endpoint for bot's avatar
            bot_alt_image_text (str): Alt text fot the bot's avata image.
            file_text_color (str): Color code for filename in the message (Hexadecimal)
            commit_button_color (list[float]): Color code for the link to github commit page the element must be between 0 and 1.
            commit_branch_color (str): Color code for branch name text (hexadecimal)
        """
        self.bot = bot
        self.bot_subtitle = bot_subtitle
        self.bot_image = bot_image
        self.bot_alt_image_text = bot_alt_image_text
        self.file_text_color = file_text_color
        self.commit_button_color = commit_button_color
        self.commit_branch_color = commit_branch_color

    def send_git_push_notification(self, request):
        # Message card.
        message = {
            "cardsV2": [
                {
                    "cardId": "unique-card-id",
                    "card": {
                        "header": {
                            "title": self.bot,
                            "subtitle": self.bot_subtitle,
                            "imageUrl": self.bot_image,
                            "imageType": "CIRCLE",
                            "imageAltText": self.bot_alt_image_text,
                        },
                        "sections": [],
                    },
                }
            ]
        }

        # Iterate through each commit and add the commit details in the message
        for commit in request["commits"]:
            message["cardsV2"][0]["card"]["sections"].append(
                {  # Name of the author made the commit
                    "header": "<h4> Commit: </h4>" + commit["author"]["name"],
                    "collapsible": True,
                    "uncollapsibleWidgetsCount": 3,
                    "widgets": [
                        # Comment of a specific commit.
                        self.create_commit_message(commit["message"]),
                        # To which bracnch the commit was made.
                        self.create_commit_branch_message(request["ref"]),
                        # Link to see the commit in github
                        self.create_commit_link_button(commit["url"]),
                    ]  # List of files got changed during that specific commit
                    + self.create_commit_file_list(commit["modified"]),
                }
            )

        requests.post(os.environ.get("GOOGLE_SPACE_WEBHOOK"), data=json.dumps(message))

    def create_commit_file_list(self, filenames):
        """
        Returns a list of text components for the message.

        Parameters:
            filenames (list[str]): list of modified file's names.
        """
        return [
            {
                "textParagraph": {
                    "text": f'<b>Files changed: </b> <font color="{self.file_text_color}">{filename}</font>'
                }
            }
            for filename in filenames
        ]

    def create_commit_link_button(self, url):
         """
        Returns a button components for the message.

        Parameters:
            url (str): url to that specific commit.
        """
        return {
            "buttonList": {
                "buttons": [
                    {
                        "text": "See Commit",
                        "onClick": {"openLink": {"url": url}},
                        "color": {
                            "red": self.commit_button_color[0],
                            "green": self.commit_button_color[1],
                            "blue": self.commit_button_color[2],
                            "alpha": self.commit_button_color[3],
                        },
                    }
                ]
            }
        }

    def create_commit_message(self, message):
        return {"textParagraph": {"text": f"<b>Message:</b> {message}"}}

    def create_commit_branch_message(self, branch_reference):
        branch = branch_reference.replace("refs/heads/", "")
        return {
            "textParagraph": {
                "text": f'<b>Branch: </b><font color="{self.commit_branch_color}">{branch}</font>'
            }
        }
