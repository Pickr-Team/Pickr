from test_login import TestLogin
from test_changePassword import TestChangePassword
from test_managerSetDeadline import TestManagerSetDeadline
from test_managerSetNotes import TestManagerSetNotes
from test_manager_set_types import TestManagerSetTypes
from test_managerViewStudentSelection import TestManagerViewStudentSelection
from test_managerViewTopics import TestManagerViewTopics
from test_studentCreateCustomTopic import TestStudentCreateCustomTopic
from test_studentSelectTopics import TestStudentSelectTopics
from test_supervisor_create_topic import TestSupervisorcreatetopic
from test_supervisorViewSelectionResult import TestSupervisorViewSelectionResult
from test_topic_list import TestTopicList


def run_tests():
    testChangePassword = TestChangePassword()
    testChangePassword.setUp()
    testChangePassword.managerLogin()
    testChangePassword.test_changePassword()
    testChangePassword.tearDown()

    testLogin = TestLogin()
    testLogin.setUp()
    testLogin.test_login()
    testLogin.tearDown()

    # TODO
    # testManagerSetDeadline = TestManagerSetDeadline()
    # testManagerSetDeadline.setUp()
    # testManagerSetDeadline.managerLogin()
    # testManagerSetDeadline.test_managerSetDeadlin()
    # testManagerSetDeadline.tearDown()

    testManagerSetNotes = TestManagerSetNotes()
    testManagerSetNotes.setUp()
    testManagerSetNotes.managerLogin()
    testManagerSetNotes.test_managerSetNotes()
    testManagerSetNotes.tearDown()

    _TestManagerSetTypes = TestManagerSetTypes()
    _TestManagerSetTypes.setUp()
    _TestManagerSetTypes.managerLogin()
    _TestManagerSetTypes.test_manager_set_types()
    _TestManagerSetTypes.tearDown()

    testManagerViewStudentSelection = TestManagerViewStudentSelection()
    testManagerViewStudentSelection.setUp()
    testManagerViewStudentSelection.managerLogin()
    testManagerViewStudentSelection.test_managerViewStudentSelection()
    testManagerViewStudentSelection.tearDown()

    testManagerViewTopics = TestManagerViewTopics()
    testManagerViewTopics.setUp()
    testManagerViewTopics.managerLogin()
    testManagerViewTopics.test_managerViewTopics()
    testManagerViewTopics.tearDown()

    testStudentCreateCustomTopic = TestStudentCreateCustomTopic()
    testStudentCreateCustomTopic.setUp()
    testStudentCreateCustomTopic.studentLogin()
    testStudentCreateCustomTopic.test_studentCreateCustomTopic()
    testStudentCreateCustomTopic.tearDown()

    testStudentSelectTopics = TestStudentSelectTopics()
    testStudentSelectTopics.setUp()
    testStudentSelectTopics.studentLogin()
    testStudentSelectTopics.test_studentSelectTopics()
    testStudentSelectTopics.tearDown()

    testSupervisor_create_topics = TestSupervisorcreatetopic()
    testSupervisor_create_topics.setUp()
    testSupervisor_create_topics.supervisorLogin()
    testSupervisor_create_topics.test_supervisorcreatetopic()
    testSupervisor_create_topics.tearDown()

    testSupervisorViewSelectionResults = TestSupervisorViewSelectionResult()
    testSupervisorViewSelectionResults.setUp()
    # testSupervisorViewSelectionResults.supervisorLogin()
    testSupervisorViewSelectionResults.test_supervisorViewSelectionResult()
    testSupervisorViewSelectionResults.tearDown()

    test_topic_list = TestTopicList()
    test_topic_list.setUp()
    test_topic_list.test_topic_list()
    test_topic_list.tearDown()


run_tests()
print("ALl tests pass!")
