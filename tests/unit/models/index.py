import unittest

from test_type import TestType
from test_note import TestNote
from test_deadline import TestDeadline
from test_student import TestStudent
from test_supervisor import TestSupervisor
from test_selection import TestSelection
from test_topic import TestTopic

suite_type = unittest.TestLoader().loadTestsFromTestCase(TestType)
suite_note = unittest.TestLoader().loadTestsFromTestCase(TestNote)
suite_deadline = unittest.TestLoader().loadTestsFromTestCase(TestDeadline)
suite_student = unittest.TestLoader().loadTestsFromTestCase(TestStudent)
suite_supervisor = unittest.TestLoader().loadTestsFromTestCase(TestSupervisor)
suite_selection = unittest.TestLoader().loadTestsFromTestCase(TestSelection)
suite_topic = unittest.TestLoader().loadTestsFromTestCase(TestTopic)

top_suite = unittest.TestSuite([suite_type, suite_note, suite_deadline, suite_student, suite_supervisor, suite_selection, suite_topic])


if __name__ == '__main__':
    # verbose mode == 2: show details of the test results
    unittest.TextTestRunner(verbosity=2).run(top_suite)