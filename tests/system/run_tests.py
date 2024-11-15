from test_login import TestLogin
from test_changePassword import TestChangePassword
from test_managerSetDeadline import TestManagerSetDeadline
from test_managerSetNotesTypes import TestManagerSetNotesTypes
from test_managerViewStudentSelection import TestManagerViewStudentSelection
from test_managerViewTopics import TestManagerViewTopics
from test_studentCreateCustomTopic import TestStudentCreateCustomTopic
from test_studentSelectTopics import TestStudentSelectTopics
from test_supervisor_create_topic import TestSupervisorcreatetopic
from test_supervisorViewSelectionResult import TestSupervisorViewSelectionResult
from test_topic_list import TestTopicList


def run_tests():
    # testChangePassword = TestChangePassword()
    # testChangePassword.test_changePassword()
    # testChangePassword.tearDown()

    testLogin = TestLogin()
    testLogin.test_login()
    testLogin.tearDown()

    # testManagerSetDeadline = TestManagerSetDeadline()
    # testManagerSetDeadline.test_managerSetDeadlin()
    # testManagerSetDeadline.tearDown()
    #
    # testManagerSetNotesTypes = TestManagerSetNotesTypes()
    # testManagerSetNotesTypes.test_managerSetNotesTypes()
    # testManagerSetNotesTypes.tearDown()
    #
    # testManagerViewStudentSelection = TestManagerViewStudentSelection()
    # testManagerViewStudentSelection.test_managerViewStudentSelection()
    # testManagerViewStudentSelection.tearDown()
    #
    # testManagerViewTopics = TestManagerViewTopics()
    # testManagerViewTopics.test_managerViewTopics()
    # testManagerViewTopics.tearDown()

    # testStudentCreateCustomTopic = TestStudentCreateCustomTopic()
    # testStudentCreateCustomTopic.test_studentCreateCustomTopic()
    # testStudentCreateCustomTopic.tearDown()
    #
    # testStudentSelectTopics = TestStudentSelectTopics()
    # testStudentSelectTopics.test_studentSelectTopics()
    # testStudentSelectTopics.tearDown()
    #
    # testSupervisor_create_topics = TestSupervisorcreatetopic()
    # testSupervisor_create_topics.test_supervisorcreatetopic()
    # testSupervisor_create_topics.tearDown()
    #
    # testSupervisorViewSelectionResults = TestSupervisorViewSelectionResult()
    # testSupervisorViewSelectionResults.test_supervisorViewSelectionResult()
    # testSupervisorViewSelectionResults.tearDown()
    #
    # test_topic_list = TestTopicList()
    # test_topic_list.test_topic_list()
    # test_topic_list.tearDown()


run_tests()
print("ALl tests pass!")
