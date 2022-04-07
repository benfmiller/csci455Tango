You are to design a dialog engine. You will demonstrate your code on our TangoChat file April
8th, times will be given by April 6th.

# Requirements:

    1. Include all the rules and definitions I have listed here:
        a. The Dialog engine will need to read in a TangoChat text file with the conversation defined. (10%)
            i. If the conversation has an error it should be output by the Dialog engine and ignore that line.(10%)
            ii. Comments should be ignored, start comments with a #. (10%)
            iii. My TangoChat file example file (I’ll link It in) should be uploaded and used for development. I will use a similar one for the demo day to test if everything is working properly.
        b. U, u1, u2, u3........and on and on , each of the following is each (without definitions, variables, or concepts, just user input robot output)
            i. U only (10 %)
            ii. U and U2 only (10%)
            iii. Infinite amount of U......Un (10%)
        c. ~ definitions (tilde) Example:
                ~greetings: [hello howdy "hi there"]
                u1:(third):~greetings
            Where the ~greetings variable is defined and given the three values in the square brackets. Then in the Rule when a user says “third” the robot will greet the user with one of the three choices, chosen randomly. The ~variables can be used over and over in the dialog text.
            i. The U level only (3%)
            ii. Add the ~ working at any level, u2, u3, u4 etc. the rest of the 5% will be added. (3%)
            iii. Having definitions working for robot use or user use is (2% each, 4% total)
            iv. In the options in the definitions you have single word phrases and multiple word phrases surrounded by “multi line phrase” (handling both 2%)
        d. (Concept [..] I updated the definition from their site, use mine): [ ] options, [option1, option2, option3] inside square brackets options, Example:
            Similar to the defnitions above, this is an options choice from several words, but they are not predefined by a ~variable, these are just in the rules such as the following rule: u:(hello):[hi hello "what up" sup] The robot chooses one of the four choices randomly to respond to the user.
            i. Handle single words (ex: [cold hot fine] ) (4%)
            ii. Handle phrases (ex: [“I’m cold” hot “I am fine”]) (3%)
            iii. Handling for human input
                1. The human says “cold” you find it in the list of choices (2%)
                    a. ex: u:[hot cold “I am fine”]: great
                    b. The user could say hot, cold or I am fine and the robot would reply “great”
            iv. Handling for robot input(2%)
                1. U: (how are you): [cold hot “I am fine”]
                2. The human asks how are you, and the robot chooses a random answer from “hot”, “cold”, or “I am fine”.
            v. Handling for level U only (%)
            vi. Handling for handling all levels, u2, u3, u4.......Un (2%)
            vii. Variables Be able to take input from the user and save the variable for reuse later.
                1. For user input the format is an underscore such as “My name is _”
                2. The robot output will have the variable to store the value, starts with a $ sign
                    a. U: (my name is _): Hello $name (3%)
                3. Then later if you can use the $name in another response.
                    a. U(what is my name) : $name (4%)
                    b. If the robot doesn’t know the name it will say “I don’t know” this would happen if the user says “what is my name” before they say “my name is __” (3%)
                4. Format u:(my name is _) : hello $name are you doing well
                    a. I went with this format because it was the easiest for you to handle.
                    b. To make it a little easier you only have to match up the words up to the underscore variable. So U:(I am _ years old) : you are $age years old. You only have to match up the “I am” and then save the number as the $age. Ignore the “years old”.
                    c. Assume every underscore only has one word answer for instance “my name is Hunter Lloyd” you only need to save “Hunter” in the $name variable.
        e. Capital letters in TangoChat file or user input should be ignored when matching input. No punctuation (? , . !, ect.) should be used in the TangoChatFile. (5%).

Here are the online rules, not all the rules on this page are relevant, above I have selected just a few of the many rules from the Aldebaran documentation. Somebody had this two week project as their job when they developed this dialog engine (they had more rules and more time).

http://doc.aldebaran.com/2-5/naoqi/interaction/dialog/dialog-syntax_full.html#topic-name

    • Rules, I put in two colons in our rules, easier to parse example: u:(user input) : robot output
        o http://doc.aldebaran.com/2-5/naoqi/interaction/dialog/dialog-syntax_full.html#rules

Don’t forget that the users will be creating the Tangochat files. Normal users do weird things, put spaces sometimes and no spaces other times. Make sure you can handle that.
