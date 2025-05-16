import os  # nosec
import subprocess  # nosec
import unittest

# echo "TEST" > ../.git/COMMIT_EDITMSG
# ./get_msg.py '../.git/COMMIT_EDITMSG' 'message'

# First install me :
# /opt/ansible/env38/bin/python3 setup.py install
# python3 setup.py install


class TestPackage(unittest.TestCase):
    def setUp(self):
        self.local_test_dir = os.path.dirname(os.path.realpath(__file__))

    def run_get_msg(self, cwd, bin, message, env=None):
        command = "{} {}".format(bin, message)

        result, err = subprocess.Popen(
            [command],
            cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,  # nosec
            env=env,
        ).communicate()

        self.assertFalse(err, "Expected no error but was " + str(err))

        return result

    def test_message(self):
        cwd = self.local_test_dir
        binary = "../bin/get_msg"
        message = "data"

        result = self.run_get_msg(cwd=cwd, bin=binary, message=message)
        self.assertIn(
            "This is doing nothing and exit with error 7",
            str(result),
        )


if __name__ == "__main__":
    unittest.main()
