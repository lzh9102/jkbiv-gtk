import re

def parseKeySequence(keyseq):
    """ Parse the key sequence string and return a Keystroke() list.
        Returns None when parsing failed.
    """
    keystrokes = []
    while len(keyseq) > 0:
        if keyseq[0] == '\\': # escape next character
            keystr = keyseq[0:2]
            keyseq = keyseq[2:]
        else:
            match = re.match(r"^<([^>]+)>", keyseq)
            if match: # found a non-displayable key (e.g. "<C-x>")
                keystr = match.group(1) # string inside <>
                keyseq = keyseq[len(match.group(0)):] # remove <...>
            else:
                keystr = keyseq[0] # the leading character
                keyseq = keyseq[1:] # remove the leading character
        if ' ' in keystr: # no space allowed in key sequence
            return None
        try:
            keystroke = Keystroke(keystr)
            keystrokes.append(keystroke)
        except:
            return None
    return keystrokes

class Keystroke(object):

    def __init__(self, keystr):
        ctrl = False
        meta = False
        shift = False
        # parse modifier
        while True:
            # match "C-" or "S-" or "M-" at the beginning of the string
            match = re.match(r"^([CcSsMm])-", keystr)
            if match:
                modifier = match.group(1).upper() # normalize to upper case
                if modifier == "C":
                    ctrl = True
                elif modifier == "S":
                    shift = True
                elif modifier == "M":
                    meta = True
                keystr = keystr[len(match.group(0)):] # remove the modifier
            else: # no more modifiers
                break
        self.key = keystr.lower() # keys are normalized to upper case
        self.ctrl = ctrl
        self.meta = meta
        self.shift = shift

    def __eq__(self, other):
        return self.key == other.key \
            and self.ctrl == other.ctrl \
            and self.meta == other.meta \
            and self.shift == other.shift

    def __hash__(self):
        return hash((self.key, self.ctrl, self.meta, self.shift))

    def __str__(self):
        kstr = ""
        if self.ctrl:
            kstr += "C-"
        if self.shift:
            kstr += "S-"
        if self.meta:
            kstr += "M-"
        kstr += self.key
        return kstr

    def __repr__(self):
        return "Keystroke(%s)" % str(self)

class ActionNode(object):

    def __init__(self):
        self.children = None

    def setAction(self, callback, *args):
        self.action = callback
        self.args = args

    def hasAction(self):
        return self.action != None

    def fire(self):
        if self.action:
            self.action(*self.args)

    def createChild(self, keystroke):
        if not self.children:
            self.children = dict()
        child = ActionNode()
        self.children[keystroke] = child
        return child

    def getChild(self, keystroke):
        if self.children:
            return self.children.get(keystroke, None)
        else:
            return None

    def hasChild(self):
        return self.children != None

class ShortcutMapper(object):

    def __init__(self):
        self.rootNode = ActionNode()
        self.queue = []

    def getNode(self, keystrokes, create):
        """ Get the node mapped to keystrokes. """
        assert(type(keystrokes) == list)
        node = self.rootNode
        for key in keystrokes:
            assert(type(key) == Keystroke)
            child = node.getChild(key)
            if child == None:
                if create:
                    child = node.createChild(key)
                else:
                    return None
            node = child
        return node

    def bind(self, keystrokes, callback, *args):
        node = self.getNode(keystrokes, create=True)
        node.setAction(callback, *args)

    def unbind(self, keystrokes):
        raise Exception("unbind() not implemented")

    def pressKey(self, keystroke):
        assert(type(keystroke) == Keystroke)
        self.queue.append(keystroke)
        node = self.getNode(self.queue, create=False)
        if node:
            if not node.hasChild(): # leaf node
                node.fire()
                self.resetState()
        else: # undefined mapping
            self.resetState()
            return False
        return True

    def resetState(self):
        self.queue[:] = [] # clear python list in place

    def clearAll(self):
        """ remove all shortcuts """
        # throw away old root node
        self.rootNode = ActionNode()

    def queuedKeys(self):
        return self.queue[:] # copy
