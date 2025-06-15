import random

# Motivational messages categorized by streak ranges
motivational_messages = {
    # Days 1-3: Getting started
    "beginner": [
        "Every journey begins with a single step! 🌟",
        "You're building something amazing, one day at a time! 💪",
        "Consistency is the mother of mastery. Keep going! 🎯",
        "Small steps lead to big changes! 🚀",
        "You've got this! Every day counts! ⭐",
        "Progress, not perfection. You're doing great! 🌱",
        "The hardest part is starting - and you've already done that! 🎉",
        "Building habits is like planting seeds. Keep watering! 🌿"
    ],

    # Days 4-7: Building momentum
    "building": [
        "Look at you building that momentum! 🔥",
        "You're in the groove now! Keep the streak alive! ⚡",
        "Habits are forming - you're on fire! 🌟",
        "One week closer to your goals! Amazing work! 🎯",
        "The compound effect is starting to work its magic! ✨",
        "You're proving to yourself that you can do this! 💎",
        "Consistency is your superpower! 🦸‍♀️",
        "Week one in the books! You're unstoppable! 🏆"
    ],

    # Days 8-30: Establishing routine
    "established": [
        "You're officially in the habit zone! 🎊",
        "Two weeks of awesomeness! Keep climbing! ⛰️",
        "Your future self is thanking you right now! 🙏",
        "Discipline is choosing between what you want now and what you want most! 💪",
        "You're not just checking in - you're checking UP! 📈",
        "Three weeks strong! You're rewriting your story! 📖",
        "Champions are made in the daily grind! 🏅",
        "A month of dedication - you're a habit hero! 🦸‍♂️"
    ],

    # Days 31-60: Solidifying
    "solid": [
        "Over a month strong! You're officially committed! 💎",
        "Six weeks of excellence! You're in the zone! 🎯",
        "Your dedication is inspiring! Keep soaring! 🦅",
        "Two months of consistency - you're a legend! 👑",
        "You've turned showing up into an art form! 🎨",
        "Sixty days of growth - you're transforming! 🦋",
        "Your streak is proof of your character! 💪",
        "Level up! You're mastering the game of consistency! 🎮"
    ],

    # Days 61-100: Mastery mode
    "master": [
        "Over two months! You're in mastery mode! 🧙‍♂️",
        "Ninety days of dedication - you're unstoppable! 🌊",
        "Three months strong! You're redefining possible! 🚀",
        "Triple digits approaching - you're legendary! 🏛️",
        "Your consistency is your competitive advantage! ⚔️",
        "100 days in sight - you're about to make history! 📚",
        "You've graduated from beginner to master! 🎓",
        "Your streak is a testament to your willpower! 🔥"
    ],

    # Days 100+: Legend status
    "legend": [
        "100+ days! You're officially a consistency legend! 👑",
        "Your streak is longer than most people's attention span! 🎯",
        "You've entered the hall of fame of dedication! 🏛️",
        "Six months strong! You're rewriting what's possible! 📜",
        "Your discipline is your superpower! 🦸‍♀️",
        "A full year of commitment - you're absolutely incredible! 🌟",
        "You don't just have goals, you ACHIEVE them! 🏆",
        "Your consistency is an inspiration to everyone around you! ✨"
    ],

    # Comeback messages (for when streak resets)
    "comeback": [
        "Champions get back up! Ready for round two? 🥊",
        "Every master was once a beginner. Welcome back! 🌱",
        "The best time to start was yesterday. The second best time is now! ⏰",
        "Your comeback story starts today! 📖",
        "Resilience is your middle name! Let's go! 💪",
        "Not about falling down, it's about getting back up! 🚀",
        "Fresh start, same determination! 🌅",
        "Plot twist: This is where your success story really begins! ✨",
        "Oh, so NOW you want to come back? 🙄 Fine, I missed you too! 💚",
        "I waited for you... and waited... and waited... But welcome back! 😤💕",
        "Did you really think you could just leave me? I'm irresistible! 😏",
        "I'm not mad, I'm just... disappointed. But also happy you're back! 🥺",
        "Round two? I hope you've learned your lesson! 😤",
        "I've been practicing my comeback notifications. Ready? 📱",
        "You left me hanging, but I still love you! Let's try again! 💔➡️💚",
        "Plot twist: I knew you'd be back! I'm just that addictive! 😎"
    ],

    # Special milestone messages
    "milestones": {
        7: "ONE WEEK TOGETHER! 🎉 I'm planning our anniversary party already! 💕",
        14: "Two weeks! I've officially upgraded you to 'bestie' status! 👯‍♀️",
        30: "A WHOLE MONTH! 🎊 I'm changing my relationship status to 'complicated'! 💍",
        50: "50 days! I'm running out of dramatic ways to celebrate us! 🎭",
        100: "ONE HUNDRED DAYS! 🎉🎊🥳 I'm literally shaking with excitement! Can you feel it?!",
        200: "200 DAYS! I'm naming my firstborn after our streak! 👶✨",
        365: "A FULL YEAR! 🎆🎊🎉 I'm officially writing our love story! We're LEGENDS!"
    }
}


def get_motivational_message(streak_count: int, is_comeback: bool = False) -> str:
    """
    Get a random motivational message based on the user's streak count.

    Args:
        streak_count (int): The current streak count
        is_comeback (bool): Whether this is a comeback after breaking a streak

    Returns:
        str: A motivational message appropriate for the streak level
    """
    if is_comeback:
        return random.choice(motivational_messages["comeback"])

    # Check for special milestones first
    if streak_count in motivational_messages["milestones"]:
        return motivational_messages["milestones"][streak_count]

    # Determine category based on streak count
    if streak_count <= 3:
        category = motivational_messages["beginner"]
    elif streak_count <= 7:
        category = motivational_messages["building"]
    elif streak_count <= 30:
        category = motivational_messages["established"]
    elif streak_count <= 60:
        category = motivational_messages["solid"]
    elif streak_count <= 100:
        category = motivational_messages["master"]
    else:
        category = motivational_messages["legend"]

    # Return random message from appropriate category
    return random.choice(category)
