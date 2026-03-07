# questions.py

# Cybersecurity Risk Assessment Tool
# Copyright (c) 2026 David Zilberman
# Licensed under the MIT License

questions = [

    # IDENTIFY
    {
        "id": 1,
        "question": "Do you maintain an up-to-date inventory of all hardware and software assets?",
        "category": "Identify",
        "weight": 10
    },

    {
        "id": 2,
        "question": "Do you perform regular cybersecurity risk assessments?",
        "category": "Identify",
        "weight": 15
    },

    # PROTECT
    {
        "id": 3,
        "question": "Do you enforce multi-factor authentication (MFA) for all users?",
        "category": "Protect",
        "weight": 20
    },

    {
        "id": 4,
        "question": "Do you require strong password policies (length, complexity, rotation)?",
        "category": "Protect",
        "weight": 15
    },

    {
        "id": 5,
        "question": "Is sensitive data encrypted at rest and in transit?",
        "category": "Protect",
        "weight": 20
    },

    # DETECT
    {
        "id": 6,
        "question": "Do you use intrusion detection or monitoring systems?",
        "category": "Detect",
        "weight": 15
    },

    {
        "id": 7,
        "question": "Are system logs reviewed regularly?",
        "category": "Detect",
        "weight": 10
    },

    # RESPOND
    {
        "id": 8,
        "question": "Do you have a documented incident response plan?",
        "category": "Respond",
        "weight": 15
    },

    {
        "id": 9,
        "question": "Do you conduct cybersecurity incident response drills?",
        "category": "Respond",
        "weight": 10
    },

    # RECOVER
    {
        "id": 10,
        "question": "Do you maintain regular, tested data backups?",
        "category": "Recover",
        "weight": 25
    },

    {
        "id": 11,
        "question": "Do you have a disaster recovery plan with defined RTO/RPO?",
        "category": "Recover",
        "weight": 20
    }

]