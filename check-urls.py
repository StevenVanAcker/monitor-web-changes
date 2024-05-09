#!/usr/bin/env python3

import hashlib
import os
import requests


class URLChecker():
    def __init__(self, urlfile: str, cachedir: str):
        self.urlfile = urlfile
        self.cachedir = cachedir

        # update cachedir to be an absolute path relative to the script
        if not os.path.isabs(self.cachedir):
            self.cachedir = os.path.join(
                os.path.dirname(__file__), self.cachedir)

    def readURLs(self):
        """
        Read the URLs from self.urlfile.
        The config file is a text file with one URL per line.
        Comments are allowed and start with a # as the first
        character on the line.
        Empty lines and comment lines are ignored.
        """

        with open(self.urlfile, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                yield line

    def contentHasChanged(self, url: str, content: bytes):
        """
        Verify whether the content of the URL has changed with
        regard to the cached content.
        Return True if the content has changed, False otherwise.
        If the URL is not cached, return True.
        The cache is updated with the new content if it has changed.
        """

        # calculate hash of the URL and the content
        urlhash = hashlib.sha256(url.encode()).hexdigest()
        contenthash = hashlib.sha256(content).hexdigest()

        # compose the cache file path
        cachefilename = f"{urlhash}.url"
        cachepath = os.path.join(self.cachedir, cachefilename)

        # Read the old content hash from the cache file if it exists
        oldcontenthash = None
        try:
            with open(cachepath, 'r') as f:
                oldcontenthash = f.read().strip()
        except FileNotFoundError:
            pass

        # Update the cache if the content has changed
        if oldcontenthash != contenthash:
            # if the cachedirectory does not exist, create it
            if not os.path.exists(self.cachedir):
                os.makedirs(self.cachedir)

            with open(cachepath, 'w') as f:
                f.write(contenthash)
            return True

        return False

    def checkURL(self, url: str):
        """
        Fetch the given URL, and determine whether the contents has changed.
        Return True if the content has changed, False otherwise.
        """

        response = requests.get(url)
        if response.status_code != 200:
            contents = b""
        else:
            contents = response.content

        # check whether the content has changed
        return self.contentHasChanged(url, contents)

    def run(self):
        """
        Check the status of every URL in the URL list.
        If any URL has changed, print an informative
        summary message to the console.
        Otherwise, output nothing.
        """

        changed = []
        for url in self.readURLs():
            if self.checkURL(url):
                changed.append(url)

        if changed:
            print("The following URLs have changed:")
            for url in changed:
                print(f"  - {url}")


if __name__ == "__main__":
    thisdirectory = os.path.dirname(__file__)
    urlsfile = os.path.join(thisdirectory, "urls.txt")
    cachedir = os.path.join(thisdirectory, "cache")
    URLChecker(urlsfile, cachedir).run()
