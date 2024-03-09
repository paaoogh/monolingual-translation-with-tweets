import logging
import os
import pandas as pd
import numpy as np

import twint as tw

from function_validators import (
    check_dataframe_integrity,
    check_date_integrity_dataframe,
)

__all__ = ["TwitterScrapper"]


class TwitterScrapper:
    FILE_NAME = "user_file"
    USER_COLUMNS_ACCEPTED = ["Usuario", "usuario", "User", "user"]
    SAVING_EXTENSION = "file_to_save_extension"
    DEFAULT_EXTENSION = ".npy"
    ENCODING_FIELD = "encoding"
    DEFAULT_ENCODING = "utf-8"
    OUT_FILE = "file_to_save_name"
    DEFAULT_OUT_FILE = "results.npy"

    def __init__(self, params: dict):
        self.params = params
        self.user_file = params.get(self.FILE_NAME, None)
        self.file_to_save = params.get(self.OUT_FILE, self.DEFAULT_OUT_FILE)
        self.encoding = params.get(self.ENCODING_FIELD, self.DEFAULT_ENCODING)

        self.users = pd.read_csv(self.user_file)
        self.users.index = range(len(self.users))

    def preprocess(self, df, f_out) -> pd.DataFrame:
        missing = df[df["Usuario"].isnull() is True]
        df = df[df["Usuario"].isnull() is False]
        name = f_out[15:-4] + "_missing.csv"
        missing.to_csv("Usuarios/" + name)
        return df

    @check_dataframe_integrity
    @check_date_integrity_dataframe
    def get_replies(self, date_since: str, username: str) -> pd.DataFrame:
        replies = tw.Config()
        replies.Since = date_since
        replies.Pandas = True
        replies.To = username
        replies.Hide_output = True
        tw.run.Search(replies)
        return tw.storage.panda.Tweets_df

    def save_replies(self, file: str, filename: str, encoding) -> pd.DataFrame:
        columnas = file.columns
        data = pd.DataFrame(columns=columnas)

        _, extension = os.path.splitext(filename)
        for person in file.index:
            logging.info("Retrieving replies to: {person}")
            date_from = file.loc[person]["Fecha de inicio"]
            username = file.iloc[person][2][1:]
            data = data.append(self.get_replies(date_from, username))

        if extension == self.DEFAULT_EXTENSION:
            np.save(filename, data.values)
        else:
            data.to_csv(filename, encoding=encoding)

    @check_dataframe_integrity
    def main_loop(self):
        logging.info(f"Leyendo {self.user_file}")
        existing_users = self.preprocess(self.users, self.file_to_save)
        self.save_replies(existing_users, self.file_to_save, self.encoding)
