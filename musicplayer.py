import os
import os.path
import pygame as pg


class Player:
    def __init__(self, book=0, chapter=0, position=0):
        # Not sure how to find this out in python
        # The files I have happen to be be at 16kHz
        pg.mixer.init(16000)

        self._book = book
        self._chapter = chapter
        self._pos = position


    @property
    def is_playing(self):
        return pg.mixer.music.get_busy()
    
    @property
    def book(self):
        """Index of the current book"""
        return self._book
    
    @book.setter
    def book(self, value):
        value %= len(self.get_file_paths())
        if self._book != value:
            print("Book = " + str(value))
            self._book = value
            self.chapter = self.position = 0
    
    @property
    def chapter(self):
        """Index of the current chapter"""
        return self._chapter
    
    @chapter.setter
    def chapter(self, value):
        value %= len(self.get_file_paths()[self.book])
        if self._chapter != value:
            print("Chapter = " + str(value))
            self._chapter = value
            self.position = 0
    
    @property
    def position(self):
        """The current position in seconds within the track"""

        # is_playing check prevents problem where there's a delay
        # between stopping playback and mixer position reset
        if self.is_playing:
            self._pos + max(0, int(pg.mixer.music.get_pos() / 1000))
        else:
            return self._pos
    
    @position.setter
    def position(self, value):
        value = max(value, 0)
        self._pos = value

        if self.is_playing:
            pg.mixer.music.stop()
            self.play()


    def get_file_paths(self):
        dirs = os.walk('audio')
        dirs_with_files = ((path, files) for path, _, files in dirs if files)
        mp3_files = (
            sorted(os.path.join(path, f) for f in files if f.endswith('.mp3'))
            for path, files in dirs_with_files
        )
        return sorted(mp3_files)


    def play(self):
        self.print_status()
        if self.is_playing:
            return

        track = self.get_file_paths()[self.book][self.chapter]
        pg.mixer.music.load(track)
        pg.mixer.music.play(start=self.position)
    
    def stop(self):
        self.position += 0
        pg.mixer.music.stop()
    
    def skip_back_chapter(self):
        """
        Convenience function for skipping back to last track (or beginning of the current track)
        """
        if self.position >= 3:
            self.position = 0
        else:
            self.chapter -= 1
    
    def skip_back_book(self):
        """
        Convenience function for skipping back to the last book (or beginning of the current book)
        """
        if self.chapter or self.position >= 30:
            self.chapter = self.position = 0
        else:
            self.book -= 1
    

    def print_status(self):
        print("Book:\t{}\nChapter:\t{}\nPosition:\t{}".format(self.book, self.chapter, self.position))


if __name__ == "__main__":
    player = Player(position=1750)
    player.play()

    while True:
        pg.time.wait(50)
        if not player.is_playing:
            player.chapter += 1
            player.play()
