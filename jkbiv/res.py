import os

# all extensions should be in lower case
EXTENSIONS = ["jpg", "png", "bmp"]

class ResourceInfo(object):

    def __init__(self, **kwargs):
        self.url = kwargs.get("url", None)
        if not self.url:
            raise TypeError("ResourceInfo() missing required kwarg 'url'")
        self.name = kwargs.get("name", os.path.basename(self.url))

    def getName(self):
        return self.name

    def getUrl(self):
        return self.url

class BaseResourceWalker(object):

    def next(self):
        return False

    def prev(self):
        return False

    def currentResource(self):
        """ returns the ResourceInfo of the current resource """
        return None

class DirectoryWalker(BaseResourceWalker):

    def __init__(self, path):
        path = os.path.abspath(path)
        # decide the directory to walk and the starting file
        if os.path.isfile(path):
            # if `path` is a file, then walk its parent directory
            self.directory = os.path.dirname(path)
            filename = os.path.basename(path)
        elif os.path.isdir(path):
            # `path` is a directory
            self.directory = path
            filename = None
        else:
            raise IOError()
        self.index = 0
        self.extensions = EXTENSIONS
        self.__refresh(origFile=filename)

    def __refresh(self, origFile=None):
        files = []
        for f in sorted(os.listdir(self.directory)):
            filename = os.path.join(self.directory, f)
            base, ext = os.path.splitext(filename)
            ext = ext[1:].lower() # remove the dot, e.g. ".jpg" => "jpg"
            if os.path.isfile(filename) and ext in self.extensions:
                files.append(f)
        self.index = files.index(origFile) if origFile in files else 0
        self.files = files

    def next(self):
        if self.index < len(self.files) - 1:
            self.index += 1
            return True
        else:
            return False

    def prev(self):
        if self.index > 0:
            self.index -= 1
            return True
        else:
            return False

    def currentResource(self):
        if self.index >= 0 and self.index < len(self.files):
            url = os.path.join(self.directory, self.files[self.index])
            res = ResourceInfo(url=url)
            return res
