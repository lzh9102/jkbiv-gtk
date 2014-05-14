from jkbiv.shortcut import *
import unittest

def KS(kstr):
    """ convert a keystroke string to Keystroke() """
    return Keystroke(kstr)

def KSL(kstr):
    """ convert a series of space-separated keystrokes to Keystroke() list """
    return [KS(key) for key in kstr.split(" ")]

class HelperFunctionsTest(unittest.TestCase):

    def testKSL(self):
        """ ensure KSL() is correct """
        self.assertEqual(KSL("C-s"), [Keystroke("C-s")])
        self.assertEqual(KSL("C-c C-x"), [Keystroke("C-c"), Keystroke("C-x")])

    def testParseKeySequence(self):
        self.assertEqual(parseKeySequence("<C-s>"),
                         KSL("C-s"))
        self.assertEqual(parseKeySequence("gu"),
                         KSL("g u"))
        self.assertEqual(parseKeySequence("<C-x>g"),
                         KSL("C-x g"))
        self.assertEqual(parseKeySequence("g<A-x>"),
                         KSL("g A-x"))
        self.assertEqual(parseKeySequence("a b"), None) # space not allowed

class KeystrokeTest(unittest.TestCase):

    def testParsing(self):
        # single key
        ks = Keystroke("a")
        self.assertEqual((ks.ctrl, ks.meta, ks.shift), (False, False, False))
        # case insensitivity
        self.assertEqual(ks.key, Keystroke("A").key)
        self.assertEqual(Keystroke("c-a"), Keystroke("C-A"))
        # key with modifier
        ks = Keystroke("c-b")
        self.assertEqual((ks.ctrl, ks.meta, ks.shift), (True, False, False))
        ks = Keystroke("M-g")
        self.assertEqual((ks.ctrl, ks.meta, ks.shift), (False, True, False))
        ks = Keystroke("s-a")
        self.assertEqual((ks.ctrl, ks.meta, ks.shift), (False, False, True))
        # multiple modifiers
        ks = Keystroke("s-c-b")
        self.assertEqual((ks.ctrl, ks.meta, ks.shift), (True, False, True))
        self.assertEqual(Keystroke("s-m-b"), Keystroke("m-s-b"))

class ActionNodeTest(unittest.TestCase):

    def testActionFire(self):
        node = ActionNode()
        self.lastAction = None
        def f1(x):
            self.lastAction = "f1(%d)" % x
        node.setAction(f1, 5)
        node.fire()
        self.assertEqual(self.lastAction, "f1(5)")
        self.assertFalse(node.hasChild())

class ShortcutMapperTest(unittest.TestCase):

    def testAction(self):
        mapper = ShortcutMapper()
        self.lastAction = None
        # callback functions
        def f1():
            self.lastAction = "f1()"
        def f2(x):
            self.lastAction = "f2(%d)" % x
        # mapping
        mapper.bind(KSL("C-c C-s"), f1)
        mapper.bind(KSL("C-c C-x"), f2, 3)

        mapper.pressKey(KS("C-c"))
        self.assertEqual(self.lastAction, None)
        self.assertListEqual(mapper.queuedKeys(), KSL("C-c"))
        mapper.pressKey(KS("C-s"))
        self.assertEqual(self.lastAction, "f1()")
        self.assertListEqual(mapper.queuedKeys(), [])

        self.lastAction = None
        mapper.pressKey(KS("C-c"))
        self.assertEqual(self.lastAction, None)
        self.assertListEqual(mapper.queuedKeys(), KSL("C-c"))
        mapper.pressKey(KS("C-x"))
        self.assertEqual(self.lastAction, "f2(3)")
        self.assertListEqual(mapper.queuedKeys(), [])

        self.lastAction = None
        mapper.pressKey(KS("C-x"))
        self.assertEqual(self.lastAction, None)
        self.assertListEqual(mapper.queuedKeys(), [])

        mapper.pressKey(KS("C-c"))
        self.assertEqual(self.lastAction, None)
        self.assertListEqual(mapper.queuedKeys(), KSL("C-c"))
        mapper.pressKey(KS("C-a")) # not mapped
        self.assertEqual(self.lastAction, None)
        self.assertListEqual(mapper.queuedKeys(), [])
