How to Contribute
=================

Contribution Guidelines
-------------------------

We welcome contributions from our community! Possible contributions may be:

  - Submit a bug report or a feature request. We are using GitHub issues as an issue tracker (see below).
  - Fix bugs in GitHub issues or implement new feature to the framework.
  - Improve documentation by sending pull-request to the website repository. Minor fixes like correction of typos or grammatical errors are also welcomed.
  - Tell us your needs in the mailing list.
  - Report us whether you could build and run Jubatus in your environment or not, along with the model/version of CPU, OS and compiler if possible.
  - Give us a general feedback (comments, problems you faced, feature requests, etc.), or tell us how you apply (or planning to apply) Jubatus in your environment in the mailing list.
 
Issue openning policy
-------------------------

* A standard issue-opening format is preferred for our better work efficiency. Therefore, we annouce our issue openning policy here for our outside contributors below.

 * How to report the issue:

  * As for the bugs reporting, your information should be adequate for our developers to reproduce and understand the bugs

  * As for other reporting, please tell us "why this part should be improved or required refactoring", "who will be benefied", etc.

   * It is no problem to write "Because I just want it!", "It makes Jubatus Cool!", your comment here will help us to decide the importance of the issue anyway.

Pull-Request Policy
---------------------

* We always welcome your code and/or documentation contributions! Here are some rules:

 * Every pull-requests will be reviewd by one (or more) of Jubatus committers. Reviewers will be chosen according to the area of the code you contributed (see the list below).

 * After the review process, your pull-request will either be:

  * ACCEPTED: your code will be merged! Note that committers will make some minor fixes (like coding styles) to your code after merging your code.

  * NEED FIX: your idea is OK, but the code contains bugs or other functionality problems, or lacks unit tests. The reviewer will tell you what you need to be fixed.

  * REJECTED: unfortunately we reject your request in case, for example, your idea does not meet with our roadmap or your code seems violating rights of others. To avoid such cases, we recommend to discuss what you are going to work on with Jubatus committers (via issue comments, IRC or mailing list) before actually starting your work, especially in case you are trying to make big changes.

 * Please note that in accordance with our roadmap, sometimes it may take time to merge your pull-request.


Tips for Contributors
---------------------

* When contributing your code, check the following points before sending pull-request:

 * Pass the unit tests. (run ./waf --checkall)

 * Pass the coding style test (run ./waf cpplint)

 * Add unit tests for your code, if applicable. We use gtest as a unittest framework.

 * If you fixed an existing issue, please include the issue number (in format of "#XXX") in the commit log.

 * If you have implemented new algorithm, add a reference to the paper you referenced in the pull-request description.

 * Please make sure that you started your work on top of the develop branch. We only accept pull-requets sent to develop branch (NOT master).


Participate in the Mailing List
-------------------------------

Join the community! We have a mailing list in `Google Groups <http://groups.google.com/group/jubatus>`_.
You can directly communicate with other users and even developers in the list.

List of Reviewers by Area

(this table https://gist.github.com/kmaehashi/771a85be03662c515012 will be added here)
