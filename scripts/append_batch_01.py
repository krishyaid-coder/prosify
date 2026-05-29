"""
Batch 1 append script — adds 50 use-case-focused DPO pairs to formatting_pairs_v1.jsonl.

Composition:
  email_draft:    15 (5 indian_corporate, 5 us_tech_casual, 5 global_neutral)
  email_refine:   15 (5 indian_corporate, 5 us_tech_casual, 5 global_neutral)
  casual_reply:   10
  short_explain:   8
  diversity:       2 (narrative, explanatory)
  -----------------
  Total:          50
"""

import json
from pathlib import Path
from collections import Counter

ROWS = [
    # ============ EMAIL_DRAFT (15) ============
    # --- indian_corporate (5) ---
    {
        "context": "email_draft", "register": "indian_corporate",
        "prompt": "Write an email to my manager Anjali letting her know I'm not feeling well and won't be in today. I'll try to be on Slack for urgent things.",
        "rejected": "Subject: Sick Leave — Today\n\nDear Anjali,\n\nI hope you are doing well. I am writing to inform you of the following:\n\n**Status:** Unwell, unable to come in today\n**Date:** [today]\n\n**Availability:**\n- Will be on Slack for urgent matters\n- Will not be able to attend scheduled meetings\n- Will catch up on work tomorrow\n\nKindly let me know if there is anything urgent I should address.\n\nRegards,\n[Your Name]",
        "chosen": "Subject: Out sick today\n\nHi Anjali,\n\nI woke up not feeling great and don't think I should come in today. I'll try to be on Slack if anything urgent comes up, but I'll mostly be resting. Should be back tomorrow.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "indian_corporate",
        "prompt": "Email HR (Shalini) asking how the new health insurance plan covers parents and what the enrollment deadline is.",
        "rejected": "Subject: Query Regarding New Health Insurance Plan\n\nDear Shalini,\n\nI hope you are well. I have a few queries regarding the new health insurance plan:\n\n**Questions:**\n1. **Parental coverage:**\n   - Are parents covered?\n   - Coverage limits?\n   - Documentation required?\n\n2. **Enrollment:**\n   - What is the deadline?\n   - How to enroll?\n   - Required forms?\n\nKindly do the needful and revert with the details at your earliest convenience.\n\nThanks and regards,\n[Your Name]",
        "chosen": "Subject: Questions about the new health insurance plan\n\nHi Shalini,\n\nCould you help me with two quick questions about the new health insurance plan? First, how does it cover parents — is there a sum-insured limit or anything I should be aware of? And second, what's the enrollment deadline?\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "indian_corporate",
        "prompt": "Polite follow-up email to a senior colleague Vikram who I asked to review my design doc 4 days ago and haven't heard back.",
        "rejected": "Subject: Gentle Follow-up — Design Doc Review\n\nDear Vikram,\n\nI hope you are doing well. I wanted to follow up on my earlier request:\n\n**Original request:** Review of design doc\n**Date sent:** [4 days ago]\n**Status:** Awaiting feedback\n\n**Why following up:**\n- Timeline considerations for next steps\n- Want to address any concerns early\n- Available to discuss in person if helpful\n\nNo rush, but a quick update would be appreciated.\n\nKind regards,\n[Your Name]",
        "chosen": "Subject: Following up on the design doc review\n\nHi Vikram,\n\nJust a gentle nudge on the design doc I shared earlier this week — no rush, but wanted to make sure it didn't get buried. Happy to walk you through it over a quick call if that would be easier than reading it cold.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "indian_corporate",
        "prompt": "Email my reporting manager Rahul informing him that I'd like to apply for an internal transfer to the data engineering team and would value his support.",
        "rejected": "Subject: Internal Transfer — Seeking Your Support\n\nDear Rahul,\n\nI hope this message finds you well. I am writing to inform you of an important career decision:\n\n**Intent:** Apply for internal transfer\n**Target team:** Data Engineering\n\n**Reasons:**\n- Alignment with long-term career interests\n- Skills development in data domain\n- Growth opportunity within the organization\n\n**Request:**\n- Your support and guidance\n- A brief conversation at your convenience\n- Smooth transition planning\n\nI am committed to ensuring a clean handover of current responsibilities. Kindly let me know a suitable time to discuss this.\n\nWith regards,\n[Your Name]",
        "chosen": "Subject: Considering an internal transfer to data engineering — would value your input\n\nHi Rahul,\n\nI wanted to share something with you before going further. I've been thinking about applying for an internal transfer to the data engineering team — it aligns more closely with the direction I'd like my career to go. Your support would mean a lot, and I'd really value the chance to talk it through with you before I move forward.\n\nCould we find 20 minutes this week?\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "indian_corporate",
        "prompt": "Email my team announcing that Friday is going to be a working-from-home day due to local transport strikes.",
        "rejected": "Subject: Work From Home — Friday\n\nDear Team,\n\nI hope you are all doing well. Please note the following announcement:\n\n**Date:** This Friday\n**Mode:** Work From Home\n**Reason:** Local transport strikes anticipated\n\n**Expectations:**\n- Available on Slack/email during working hours\n- Attend all scheduled meetings via video\n- Maintain regular deliverables\n\n**Action items:**\n- Carry laptops home today\n- Test VPN access in advance\n- Reach out for any blockers\n\nKindly plan accordingly.\n\nRegards,\n[Your Name]",
        "chosen": "Subject: WFH on Friday — transport strikes expected\n\nHi team,\n\nGiven the transport strikes expected on Friday, let's all plan to work from home that day. Please make sure you carry your laptops home tonight and test your VPN access if you haven't recently. Meetings will go ahead as usual on video. Reach out if anything's a blocker.\n\nThanks,\n[Your Name]"
    },
    # --- us_tech_casual (5) ---
    {
        "context": "email_draft", "register": "us_tech_casual",
        "prompt": "Write a quick email to Marcus letting him know the dashboard work is going to slip by about a week — the data pipeline turned out to be messier than expected.",
        "rejected": "Subject: Dashboard Timeline Update\n\nHi Marcus,\n\nI wanted to provide an update on the dashboard project:\n\n**Status:** Behind schedule\n**New ETA:** Approximately 1 week later than original deadline\n\n**Root cause:**\n- Data pipeline complexity\n- Unexpected data quality issues\n- Additional cleaning required\n\n**Next steps:**\n- Complete pipeline fixes\n- Resume dashboard build\n- Provide weekly updates\n\nLet me know if you have any concerns.\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Dashboard slipping by ~1 week\n\nHey Marcus,\n\nQuick heads up — the dashboard is going to slip by about a week. The data pipeline turned out to be messier than I expected, with a bunch of inconsistencies I have to clean up before the dashboard queries make sense. Once that's sorted the dashboard itself should come together quickly.\n\nHappy to hop on a call if you want to talk through it.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "us_tech_casual",
        "prompt": "Email my skip-level manager Dev asking for a 30-min 1:1 sometime in the next two weeks. I want to talk about career growth.",
        "rejected": "Subject: Request for 1:1 — Career Discussion\n\nHi Dev,\n\nI wanted to request some time on your calendar:\n\n**Duration:** 30 minutes\n**Timeframe:** Within the next 2 weeks\n**Topic:** Career growth discussion\n\n**Specific topics:**\n- Long-term career path\n- Skill development priorities\n- Growth opportunities within the team\n\nPlease let me know what works for your schedule!\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Quick 30-min 1:1 in the next couple weeks?\n\nHi Dev,\n\nWould you have 30 minutes in the next two weeks for a 1:1? I'd love to chat about career growth — nothing urgent, just want to get your perspective on where I should be focusing.\n\nHappy to work around your schedule.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "us_tech_casual",
        "prompt": "Email my manager Rebecca asking to discuss a salary review at our next 1:1.",
        "rejected": "Subject: Discussion Topic for Next 1:1 — Compensation Review\n\nHi Rebecca,\n\nWanted to flag a topic I'd like to discuss in our next 1:1:\n\n**Topic:** Compensation review\n\n**Context:**\n- It's been [time] since my last review\n- I've taken on [responsibilities]\n- Want to align on growth trajectory\n\n**What I'd like to discuss:**\n- Current compensation alignment\n- Path to next level\n- Timing of formal review\n\nLet me know if you'd prefer to handle this in a separate meeting.\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Want to talk about a comp review at our next 1:1\n\nHi Rebecca,\n\nI'd like to set aside some time in our next 1:1 to talk about my compensation. It's been a while since my last review and I've picked up some new responsibilities, so it feels like the right moment to sync on where we are. Let me know if you'd rather break it into its own meeting.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "us_tech_casual",
        "prompt": "Slack-style email asking my teammate Raj if he'd swap on-call shifts with me — I have a wedding next weekend and he's on the following one.",
        "rejected": "Subject: On-call Swap Request\n\nHi Raj,\n\nHoping you might be open to an on-call swap:\n\n**Current schedule:**\n- My shift: Next weekend\n- Your shift: Following weekend\n\n**Request:**\n- Swap our shifts\n- I'd cover your weekend, you'd cover mine\n\n**Reason:**\n- I have a wedding next weekend\n- Will be unreachable for most of it\n\n**Benefit to you:**\n- One weekend earlier on call, one weekend later off\n- Happy to owe you one for future swaps\n\nLet me know if you can swing it!\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Any chance you'd swap on-call with me?\n\nHey Raj,\n\nI'm on call next weekend but I've got a wedding I really can't miss — would you be up for swapping with me? You'd take next weekend and I'd cover yours the weekend after. Owe you one either way.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "us_tech_casual",
        "prompt": "Email Sarah saying I need to head out at 3pm Thursday for my kid's parent-teacher conference.",
        "rejected": "Subject: Early Departure — Thursday\n\nHi Sarah,\n\nWanted to give you a heads up on my schedule this week:\n\n**When:** Thursday, 3:00 PM\n**Reason:** Parent-teacher conference for my child\n**Duration:** Will be out for the rest of the day\n\n**Coverage:**\n- Will complete all morning tasks\n- Available on phone if anything urgent\n- Can make up time Friday\n\nLet me know if any concerns!\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Out at 3 Thursday for a parent-teacher conference\n\nHey Sarah,\n\nJust a heads up — I'll need to head out at 3 on Thursday for a parent-teacher conference and won't be back online. I'll make sure anything time-sensitive is done before then. Reachable on phone if something blows up.\n\nThanks,\n[Your Name]"
    },
    # --- global_neutral (5) ---
    {
        "context": "email_draft", "register": "global_neutral",
        "prompt": "Email my manager Tom requesting four days off in October for my cousin's wedding. I'll plan it well in advance.",
        "rejected": "Subject: Leave Request — Family Wedding\n\nDear Tom,\n\nI hope this message finds you well. I would like to submit a leave request for the following:\n\n**Reason:** Cousin's wedding\n**Dates:** [4 days in October]\n\n**Preparation:**\n- Will provide handover documentation\n- Will brief team in advance\n- Will be available on email for emergencies\n\nPlease let me know if these dates work, and I am happy to discuss any concerns.\n\nBest regards,\n[Your Name]",
        "chosen": "Subject: Leave request — 4 days in October for a family wedding\n\nHi Tom,\n\nMy cousin is getting married in October and I'd like to take four days off around the event — I can confirm the exact dates once they're finalized. Since it's still a couple of months out, I'll have plenty of time to wrap up open work and brief whoever needs covering.\n\nLet me know if there's anything to be aware of timing-wise.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "global_neutral",
        "prompt": "Email leadership to share that we've shipped the search redesign — first week numbers look promising, engagement up 12%.",
        "rejected": "Subject: Search Redesign — Launch Update\n\nDear Leadership,\n\nI am pleased to share an update on the search redesign launch:\n\n**Status:** Shipped successfully\n**Launch date:** [date]\n\n**Initial metrics (Week 1):**\n- Engagement: +12%\n- User feedback: Positive\n- No critical bugs identified\n\n**Next steps:**\n- Continue monitoring metrics\n- Gather qualitative feedback\n- Plan iteration 2\n\nHappy to share more detail in person.\n\nBest regards,\n[Your Name]",
        "chosen": "Subject: Search redesign shipped — week-one numbers looking good\n\nHi all,\n\nQuick update — the search redesign is live, and the first week's numbers are encouraging. Engagement is up about 12% and we haven't seen any critical issues. Still early to draw firm conclusions, but the signal is in the right direction. I'll share a fuller breakdown in next week's review.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "global_neutral",
        "prompt": "I was invited to a meeting that doesn't really need me. Help me decline politely without being rude.",
        "rejected": "Here's a polite decline:\n\n**Subject:** Re: [Meeting Name]\n\n**Email:**\n\nHi [Organizer],\n\nThank you for the invitation to [meeting]. After reviewing the agenda, I don't think my presence will add value:\n\n**Reasons:**\n- Topics outside my scope\n- Other team members better positioned to contribute\n- Conflicting priorities for the time slot\n\n**Alternative:**\n- Happy to review notes afterward\n- Available for follow-up if needed\n\nThanks for understanding!\n\nBest,\n[Your Name]",
        "chosen": "Subject: Re: [meeting]\n\nHi [Name],\n\nThanks for including me. Looking at the agenda, I don't think I'd add much in the room — happy to read the notes afterward and follow up if anything needs my input. Feel free to drop me from the invite.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "global_neutral",
        "prompt": "Email a client apologizing that we missed the deadline for delivering the report by two days. Give a brief honest reason.",
        "rejected": "Subject: Apology — Delayed Report Delivery\n\nDear [Client],\n\nI'm writing to apologize for the delay in delivering the report.\n\n**Original deadline:** [date]\n**Actual delivery:** 2 days late\n\n**Reason for delay:**\n- Unexpected complexity in data analysis\n- Required additional verification\n- Quality could not be compromised\n\n**Going forward:**\n- Implementing better buffer in timelines\n- More frequent check-ins\n- Will not happen again\n\nApologies again for the inconvenience.\n\nSincerely,\n[Your Name]",
        "chosen": "Subject: Apologies — report is two days late\n\nHi [Name],\n\nI owe you an apology — the report is going out two days later than promised. The data analysis turned out to be more involved than we'd estimated, and I'd rather get it right than rush it out. The report is attached now. Happy to walk through it whenever works for you.\n\nThanks for your patience,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "global_neutral",
        "prompt": "Email to stakeholders introducing Maya, who's joining as our new PM next Monday.",
        "rejected": "Subject: Team Introduction — New Product Manager\n\nHi all,\n\nI'm excited to announce a new addition to the team:\n\n**Name:** Maya\n**Role:** Product Manager\n**Start date:** Monday, [date]\n\n**Background:**\n- Will share full bio shortly\n- Brings significant product expertise\n\n**Immediate priorities:**\n- Getting up to speed on our roadmap\n- Meeting key stakeholders\n- Shadowing current PM\n\n**Action items:**\n- Please welcome Maya\n- Add her to relevant channels\n- Schedule 1:1s during her first two weeks\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Welcoming Maya — joining as our new PM on Monday\n\nHi everyone,\n\nWanted to give you a quick heads up that Maya will be joining as our new PM next Monday. She'll be picking up the roadmap work and will be reaching out for 1:1s over her first couple of weeks. Please give her a warm welcome — and if you'd like to grab some time with her early on, feel free to ping her directly once she's on Slack.\n\nThanks,\n[Your Name]"
    },

    # ============ EMAIL_REFINE (15) ============
    # --- indian_corporate (5) ---
    {
        "context": "email_refine", "register": "indian_corporate",
        "prompt": "Polish this email I'm sending to a senior person: 'Respected Sir, I am extremely sorry to disturb you with this small matter but I was wondering if you could kindly find some time from your busy schedule to please review the attached document at your convenience. Many thanks in advance for your kindness.'",
        "rejected": "Here's a polished, more confident version:\n\n**Subject:** Document Review Request\n\n**Email Body:**\n\nDear [Sir],\n\nI hope you are doing well. I would appreciate your review of the attached document when you have a moment.\n\n**About the document:**\n- Topic: [insert]\n- Length: [pages]\n- Timeline: No urgent deadline\n\n**Specific feedback areas:**\n- Overall direction\n- Any concerns or red flags\n\nThank you for your time.\n\nBest regards,\n[Your Name]\n\n**What changed:**\n- Removed excessive apologizing\n- Made the ask clear and specific\n- Maintained respectful tone",
        "chosen": "Subject: Document for your review\n\nDear [Name],\n\nCould you take a look at the attached document when you have time? Any feedback on the direction would be valuable, but there's no urgent deadline.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "indian_corporate",
        "prompt": "Make this sound less robotic: 'Dear Team, This is to inform you that the monthly review meeting has been rescheduled from Friday to Monday at the same time. Kindly do the needful and update your calendars accordingly. Regards.'",
        "rejected": "Here's a more natural version:\n\n**Subject:** Monthly Review — Rescheduled to Monday\n\n**Email Body:**\n\nHi team,\n\nA quick scheduling update:\n\n**Change:**\n- **Original:** Friday, [time]\n- **New:** Monday, [same time]\n\n**Reason:** [Add if relevant]\n\n**Action required:**\n- Update calendars\n- Reschedule conflicts\n- Reach out with concerns\n\nThanks,\n[Your Name]\n\n**Key improvements:**\n- Removed corporate jargon\n- More conversational tone\n- Clear action items",
        "chosen": "Subject: Monthly review moved to Monday\n\nHi team,\n\nQuick heads up — the monthly review is moving from Friday to Monday, same time. Please update your calendars. Let me know if Monday creates a conflict for anyone.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "indian_corporate",
        "prompt": "Make this ask clearer and more confident: 'Dear Sir, I was just thinking maybe if it would be possible at some point, perhaps you could let me know when there might be an opportunity to discuss my role and possibly take on some new responsibilities, only if it's convenient for you of course.'",
        "rejected": "Here's a clearer, more confident version:\n\n**Subject:** Request to Discuss Role and Responsibilities\n\n**Email:**\n\nDear [Name],\n\nI'd like to set up a discussion about my role and expanding my responsibilities.\n\n**What I'd like to discuss:**\n- Current role scope\n- Areas where I could take on more\n- Path to next level\n\n**Specific interests:**\n- [Area 1]\n- [Area 2]\n- [Area 3]\n\n**Proposed:**\n- 30-minute meeting\n- Any time that works for you\n\nThanks for considering.\n\nBest regards,\n[Your Name]",
        "chosen": "Subject: Request to discuss expanding my role\n\nDear [Name],\n\nI'd like to find time in the next couple of weeks to discuss my role — specifically, taking on some additional responsibilities. Would 30 minutes work somewhere in your calendar? Happy to fit around your schedule.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "indian_corporate",
        "prompt": "Sounds too desperate, fix it: 'Respected Sir, I am writing to humbly request that you please consider me for the new internal opportunity that was posted last week. I have been working very hard and I really really want this opportunity. I would be forever grateful if you could put in a good word for me. Thanking you in advance.'",
        "rejected": "Here's a more professional, confident version:\n\n**Subject:** Interest in Internal Opportunity — [Role Name]\n\n**Email:**\n\nDear [Name],\n\nI'm writing to express my interest in the recently posted internal opportunity.\n\n**Why I'm a good fit:**\n- [Relevant experience 1]\n- [Relevant experience 2]\n- [Relevant skills]\n\n**What I'm seeking:**\n- Consideration for the role\n- Brief discussion if possible\n- Your perspective on fit\n\n**Available to:**\n- Discuss further over coffee\n- Share more context on my background\n- Address any questions\n\nThank you for considering.\n\nBest regards,\n[Your Name]",
        "chosen": "Subject: Interest in the new internal opportunity\n\nHi [Name],\n\nI saw the internal opening posted last week and I'd like to throw my hat in. I think my recent work on [project] aligns well with what the role calls for, and I'd appreciate the chance to discuss it with you. Could we find 20 minutes to talk it through?\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "indian_corporate",
        "prompt": "Tone this down — sounds too formal for a casual update to my own team: 'Dear Esteemed Team Members, I would like to take this opportunity to formally inform you all that the deployment scheduled for tonight has been postponed to tomorrow night due to certain unforeseen technical issues. Kindly take note of the same.'",
        "rejected": "Here's a more casual version suitable for a team update:\n\n**Subject:** Deployment Postponed — Now Tomorrow Night\n\n**Email:**\n\nHi team,\n\nQuick update on tonight's deployment:\n\n**Change:**\n- **Old:** Tonight\n- **New:** Tomorrow night, same time\n\n**Reason:**\n- Unforeseen technical issues\n- Need additional time to resolve\n\n**Action items:**\n- No on-call required tonight\n- Be ready for tomorrow night instead\n\n**Improvements made:**\n- Removed formal salutation\n- Conversational tone\n- Clear and direct",
        "chosen": "Subject: Tonight's deployment pushed to tomorrow\n\nHi team,\n\nTonight's deployment is being pushed to tomorrow night — we ran into some technical issues that need sorting out first. No on-call needed tonight; same plan for tomorrow.\n\nThanks,\n[Your Name]"
    },
    # --- us_tech_casual (5) ---
    {
        "context": "email_refine", "register": "us_tech_casual",
        "prompt": "This email I drafted sounds passive aggressive, can you make it more direct without being rude: 'Hi, just wondering if you got my email from last week about the budget? Would be GREAT to actually hear back so we can move forward. Thanks!!!'",
        "rejected": "Here's a more direct, professional version:\n\n**Subject:** Follow-up — Budget Question\n\n**Email:**\n\nHi [Name],\n\nI'm following up on my email from last week regarding the budget:\n\n**Original ask:** Budget approval for [project]\n**Date sent:** Last week\n**Status:** Awaiting response\n\n**Why I'm following up:**\n- Timeline pressure\n- Blocked on next steps\n- Need to inform the team\n\n**Could you let me know:**\n- Approval status\n- Any concerns to address\n- Timing for a decision\n\nThanks!\n\n[Your Name]",
        "chosen": "Subject: Following up on the budget question\n\nHi [Name],\n\nWanted to check in on the budget email I sent last week — we're blocked on a couple of next steps until we hear back. Even a rough sense of when you'd be able to weigh in would be helpful.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "us_tech_casual",
        "prompt": "Rewrite this to be confident, not apologetic: 'Hi, sorry for the bother but I was hoping maybe if it's not too much trouble, could I possibly get the analytics access I requested a couple of days ago? Sorry to chase, I know you're busy.'",
        "rejected": "Here's a more confident version:\n\n**Subject:** Analytics Access Follow-up\n\n**Email:**\n\nHi [Name],\n\nFollowing up on my analytics access request:\n\n**Original request:** [date, 2 days ago]\n**Type:** Analytics dashboard access\n**Status:** Pending\n\n**Why it matters:**\n- Blocking project work\n- Needed for upcoming deliverable\n- Team relies on the data\n\n**Could you:**\n- Confirm receipt\n- Provide ETA\n- Flag any blockers\n\nThanks for your time!\n\n[Your Name]",
        "chosen": "Subject: Following up on analytics access\n\nHi [Name],\n\nFollowing up on the analytics access I requested a couple of days ago — could you let me know where it's at? I'm blocked on a piece of work that needs it.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "us_tech_casual",
        "prompt": "The ask in this email is buried — make it clearer: 'Hey, hope your week is going well! I was thinking about the project and I had some thoughts and was wondering about the timeline and what you think the priorities should be and also if we need to involve design at this stage and stuff. Let me know what you think when you get a chance!'",
        "rejected": "Here's a clearer version with the ask up front:\n\n**Subject:** Project Planning Questions\n\n**Email:**\n\nHi [Name],\n\nI have a few questions on the project I'd like your input on:\n\n**Questions:**\n1. **Timeline:** What are we targeting?\n2. **Priorities:** What's the order of work?\n3. **Design involvement:** Bring them in now or later?\n\n**Why now:**\n- Want to align before next sprint\n- Need to plan resources\n- Avoid late-stage rework\n\n**Could we:**\n- Discuss in next 1:1?\n- Or async if you prefer\n\nThanks!\n\n[Your Name]",
        "chosen": "Subject: Three quick questions on the project\n\nHi [Name],\n\nThree things I'd love your take on whenever you have a minute: what timeline are we targeting, what should the priority order be, and do we need design involved at this stage? Happy to discuss async or in our next 1:1 — whichever's easier.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "us_tech_casual",
        "prompt": "Warm this up a little — it sounds cold: 'The numbers in your report are wrong. The Q2 figure is off by $50k. Fix it.'",
        "rejected": "Here's a warmer, more collaborative version:\n\n**Subject:** Q2 Figure Discrepancy in Report\n\n**Email:**\n\nHi [Name],\n\nHope you're doing well! I was reviewing the report and noticed something I wanted to flag:\n\n**Issue:**\n- Q2 figure appears to be off by ~$50k\n- May want to double-check the source data\n\n**Possible causes:**\n- Data refresh timing\n- Calculation error\n- Source discrepancy\n\n**Suggested next steps:**\n- Review and verify\n- Update if confirmed\n- Let me know if I'm missing context\n\nThanks for taking a look!\n\n[Your Name]",
        "chosen": "Subject: Quick flag on the Q2 figure in your report\n\nHi [Name],\n\nNoticed the Q2 figure in the report looks off — by about $50k compared to what I have. Could you double-check on your end? Might be something I'm missing on my side, but wanted to flag it before it goes out.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "us_tech_casual",
        "prompt": "Cut this in half: 'Hey team, I wanted to share a few updates from this week. First, the API work is going well — we wrapped the auth endpoints on Tuesday and are now moving to the user endpoints. Second, the design review went better than expected — the team had a lot of positive things to say about the new direction and only a couple of small concerns. Third, we have a new joiner starting next Monday so please be welcoming. Lastly, just a reminder that next Friday is our team offsite so please make sure your travel is booked.'",
        "rejected": "Here's a tighter version:\n\n**Subject:** Weekly Updates — [Date]\n\n**Email:**\n\nHi team,\n\nQuick roundup of this week:\n\n**API work:**\n- ✅ Auth endpoints wrapped Tuesday\n- 🔄 Moving to user endpoints\n\n**Design review:**\n- Went well\n- Minor concerns raised\n- Direction approved\n\n**New joiner:**\n- Starting Monday\n- Please welcome\n\n**Reminders:**\n- Team offsite next Friday\n- Book travel\n\nThanks!\n\n[Your Name]",
        "chosen": "Subject: Weekly roundup\n\nHi team,\n\nFour quick things: auth endpoints wrapped Tuesday, moving to user endpoints next. Design review went well, just a couple of minor notes. New joiner starts Monday — please be welcoming. And don't forget to book travel for the offsite next Friday.\n\nThanks,\n[Your Name]"
    },
    # --- global_neutral (5) ---
    {
        "context": "email_refine", "register": "global_neutral",
        "prompt": "Cut this down significantly: 'Hi, I hope you're doing well, I just wanted to quickly reach out and check in about the meeting we had last Thursday where we discussed the proposal for the new collaboration between our teams and I wanted to see if there had been any progress or thinking on your side since then or if there's anything I can do to help move things along or provide more information that would be useful.'",
        "rejected": "Here's a tighter version:\n\n**Subject:** Following Up — Last Thursday's Meeting\n\n**Email:**\n\nHi [Name],\n\nFollowing up on our meeting last Thursday about the team collaboration proposal:\n\n**Quick questions:**\n- Any progress on your side?\n- Anything you need from me?\n- Additional info that would help?\n\n**Happy to:**\n- Schedule another sync\n- Share more context\n- Address any blockers\n\nLet me know.\n\nBest,\n[Your Name]\n\n**Reductions:**\n- Removed unnecessary pleasantries\n- Bulleted key questions\n- Cut filler language",
        "chosen": "Subject: Quick follow-up on Thursday's collaboration discussion\n\nHi [Name],\n\nFollowing up on Thursday's chat about the team collaboration proposal — has there been any movement on your end? Happy to send more context or jump on another call if it'd help things along.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "global_neutral",
        "prompt": "Drastically shorten this: 'Dear team, I wanted to take a moment to acknowledge the incredible work everyone has put in over the past quarter. We faced numerous challenges, including the platform migration, the unexpected hiring freeze, and the shift in market priorities. Despite all of this, you have consistently delivered high-quality work and supported each other in remarkable ways. I just want to say thank you and remind everyone that your efforts are seen and appreciated.'",
        "rejected": "Here's a shorter version:\n\n**Subject:** Thank You — Q[X] Recognition\n\n**Email:**\n\nHi team,\n\nQuick note of appreciation:\n\n**Challenges faced:**\n- Platform migration\n- Hiring freeze\n- Market priority shifts\n\n**What you delivered:**\n- Consistent high-quality work\n- Strong team support\n\n**Bottom line:**\n- Your work is seen\n- Your efforts are appreciated\n- Thank you all\n\n[Your Name]\n\n**Cuts:**\n- Removed redundant phrasing\n- Bulleted main points\n- Tighter structure",
        "chosen": "Subject: Thank you\n\nHi team,\n\nJust wanted to say thank you. This past quarter threw a lot at us — the migration, the hiring freeze, the priority shifts — and you all kept showing up and doing great work. It hasn't gone unnoticed.\n\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "global_neutral",
        "prompt": "Make this sound more natural in English: 'Hi, I want to inform you regarding the project that we are working on it from last two weeks and there are some difficulties we are facing in the implementation part especially related with the API integration which is taking more time than expected.'",
        "rejected": "Here's a more natural English version:\n\n**Subject:** Project Update — API Integration Delays\n\n**Email:**\n\nHi [Name],\n\nWanted to update you on the project we've been working on for the past two weeks:\n\n**Status:**\n- Active development\n- Behind schedule on implementation\n\n**Specific challenge:**\n- API integration is taking longer than expected\n- Primary blocker for completion\n\n**What we're doing:**\n- Working through integration issues\n- May need additional time\n- Will provide updated timeline\n\n**Need from you:**\n- Awareness of delay\n- Confirmation of any flexibility on timeline\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Project update — API integration taking longer than expected\n\nHi [Name],\n\nQuick update on the project we've been working on for the past two weeks. We've hit some friction on the API integration side that's taking longer than we'd planned for. Implementation is moving, just slower than we'd hoped. I'll have a clearer revised timeline by the end of the week.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "global_neutral",
        "prompt": "This email is missing context — add what's needed: 'Hi, please send the file by tomorrow. Thanks.'",
        "rejected": "Here's a version with proper context:\n\n**Subject:** Request for [File Name] by Tomorrow\n\n**Email:**\n\nHi [Name],\n\nI hope you're doing well. I'm writing to request a specific file:\n\n**File needed:** [File name/description]\n**Deadline:** Tomorrow, [date]\n\n**Why I need it:**\n- [Purpose 1]\n- [Purpose 2]\n- Tied to upcoming deliverable\n\n**Format preferred:**\n- [File type]\n- [Any specific requirements]\n\n**If unable to send by tomorrow:**\n- Please let me know ASAP\n- Suggest alternative timeline\n\nThanks for your help!\n\nBest,\n[Your Name]",
        "chosen": "Subject: Could I get the Q3 forecast file by tomorrow?\n\nHi [Name],\n\nCould you send over the Q3 forecast file by end of day tomorrow? I need it for the presentation I'm putting together for Thursday's leadership review. If tomorrow's tight, let me know what's possible.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "global_neutral",
        "prompt": "I need to decline this collaboration invitation gracefully — it's from someone senior and I want to maintain the relationship: 'Hi Alex, sorry I really can't take on this collab, I'm slammed. Maybe next quarter.'",
        "rejected": "Here's a more graceful version:\n\n**Subject:** Re: Collaboration Opportunity\n\n**Email:**\n\nHi Alex,\n\nThank you so much for thinking of me for this collaboration.\n\n**Current situation:**\n- Bandwidth is fully committed\n- Several priority projects in flight\n- Cannot do justice to this work right now\n\n**What I can offer:**\n- Quick brainstorming call if helpful\n- Recommendations of others who might fit\n- Stay informed on progress\n\n**Future possibility:**\n- Next quarter looks more open\n- Happy to revisit then\n- Would love to find a way to work together\n\nThanks again for the opportunity!\n\nBest,\n[Your Name]",
        "chosen": "Subject: Re: collaboration opportunity\n\nHi Alex,\n\nThank you so much for thinking of me — really. Unfortunately I'm at capacity right now and wouldn't be able to give this the attention it deserves. Could we revisit early next quarter? I'd genuinely like to find a way to work together.\n\nThanks,\n[Your Name]"
    },

    # ============ CASUAL_REPLY (10) ============
    {
        "context": "casual_reply",
        "prompt": "Reply to a Slack message from my teammate: 'got a sec to look at something quick?'",
        "rejected": "Here are some reply options:\n\n**If available:**\n- Yes, what's up?\n- Sure — share it.\n- Of course, shoot.\n\n**If briefly busy:**\n- In a meeting, give me 10?\n- Hit me up in 15.\n- Yes, but quick.\n\n**Tone tips:**\n- Be responsive\n- Set expectations\n- Stay friendly",
        "chosen": "Sure, what's up?"
    },
    {
        "context": "casual_reply",
        "prompt": "Reply to a coworker who messaged: 'hey did you see my message from yesterday about the API spec?'",
        "rejected": "Here are options depending on the situation:\n\n**If you missed it:**\n- Sorry, missed it — let me read now and get back to you.\n\n**If you saw it but forgot:**\n- Sorry, I saw it but it slipped my mind. Looking now.\n\n**If you saw it and have an answer:**\n- Yes, I did — was just gathering thoughts. [Answer here]\n\n**Best practice:**\n- Be honest\n- Take ownership\n- Provide ETA if delayed",
        "chosen": "Sorry, missed it — pulling it up now. Will reply in a bit."
    },
    {
        "context": "casual_reply",
        "prompt": "Reply to a coworker who Slacked: 'lunch today? trying that new ramen place'",
        "rejected": "Here are some reply options:\n\n**If yes:**\n- Yes! What time?\n- Count me in.\n- Sounds great, meet at the lobby?\n\n**If no:**\n- Can't today, swamped. Rain check?\n- Already brought lunch, but enjoy!\n- Not today, but tomorrow?\n\n**Tone:**\n- Match their casual energy\n- Be specific if you accept\n- Offer alternative if you decline",
        "chosen": "Yes — meet at the lobby at 12:30?"
    },
    {
        "context": "casual_reply",
        "prompt": "A friend asks via WhatsApp: 'how did your big project demo go yesterday?'",
        "rejected": "Here are some response options:\n\n**If it went well:**\n- It went great! Got really good feedback, feeling relieved.\n\n**If it went okay:**\n- It went okay — some tough questions but overall fine. Glad it's done.\n\n**If it went poorly:**\n- Honestly rough. Some things didn't land. Recovering and learning.\n\n**Conversational tips:**\n- Be authentic\n- Match the relationship's intimacy\n- Invite follow-up if you want to talk",
        "chosen": "Honestly, way better than I expected. Got through the demo without anything breaking, and the questions were actually fair. Feel like I can finally exhale."
    },
    {
        "context": "casual_reply",
        "prompt": "Reply to a Slack from my manager: 'really impressive work on the launch this week, you should be proud'",
        "rejected": "Here are response options:\n\n**Gracious acceptance:**\n- Thank you, that means a lot! It was a real team effort.\n\n**Share credit:**\n- Thanks! Couldn't have done it without [teammate names].\n\n**Express gratitude with humility:**\n- Appreciate that — there's still a lot to improve, but glad the launch landed well.\n\n**Best practice:**\n- Accept the compliment gracefully\n- Share credit where due\n- Stay humble but don't deflect entirely",
        "chosen": "Thanks, that genuinely means a lot. Couldn't have pulled it off without Priya and James — they did the heavy lifting on the backend side."
    },
    {
        "context": "casual_reply",
        "prompt": "Coworker Slacks: 'hey can you take a look at this PR when you have a chance? Failing one weird test and i'm stuck'",
        "rejected": "Here are response options:\n\n**If available now:**\n- Sure, link it — looking now.\n\n**If briefly busy:**\n- Wrapping something up, give me 20 minutes and I'll dive in.\n\n**If swamped:**\n- Swamped today — can [other person] help? Otherwise tomorrow morning.\n\n**Helpful additions:**\n- Ask for context (what have they tried?)\n- Set expectations on timing\n- Offer alternatives if unavailable",
        "chosen": "Yep, send the link — I'll take a look in about 20."
    },
    {
        "context": "casual_reply",
        "prompt": "Coworker messages: 'happy birthday! hope you have a great day 🎉'",
        "rejected": "Here are response options:\n\n**Brief thanks:**\n- Thanks so much!\n\n**Warm acknowledgment:**\n- Thank you! Means a lot 🙏\n\n**With humor:**\n- Thanks! Officially one year older and wiser (allegedly).\n\n**Reciprocal:**\n- Thanks!! Hope your day is great too.\n\n**Tips:**\n- Keep it brief\n- Match their energy\n- Use emoji if they did",
        "chosen": "Thank you! 🎉 Appreciate it."
    },
    {
        "context": "casual_reply",
        "prompt": "Need to cancel lunch plans with coworker Mira last minute — something urgent came up at work. Help me message her.",
        "rejected": "Here are options:\n\n**Straightforward apology:**\n- Hey Mira, I'm so sorry — something urgent came up at work and I have to cancel lunch. Can we reschedule for later this week?\n\n**Brief and apologetic:**\n- Mira, gotta bail on lunch — work emergency. Truly sorry. Reschedule tomorrow?\n\n**More detail:**\n- Hi Mira, ugh, so sorry to do this — production issue just blew up and I can't step away. Rain check this week?\n\n**Best practice:**\n- Apologize sincerely\n- Give brief reason\n- Suggest concrete alternative",
        "chosen": "Mira, I'm so sorry — something just blew up at work and I can't step away. Can we reschedule for Thursday or Friday?"
    },
    {
        "context": "casual_reply",
        "prompt": "A coworker messaged: 'so sorry to hear about your dad, thinking of you'. Help me respond.",
        "rejected": "Here are some response options:\n\n**Brief and genuine:**\n- Thank you, that means a lot.\n\n**Slightly fuller:**\n- Thank you so much — I really appreciate it. It's been a hard week, but messages like yours help.\n\n**Acknowledging without going deep:**\n- Thank you for reaching out. Appreciate the kindness.\n\n**Tone considerations:**\n- Brevity is okay\n- Genuine over polished\n- No need to over-explain",
        "chosen": "Thank you — that really does mean a lot. It's been a tough week, and the messages help more than I can say."
    },
    {
        "context": "casual_reply",
        "prompt": "Coworker Slack: 'free to chat this afternoon?'",
        "rejected": "Here are options:\n\n**Yes:**\n- Yes! What time?\n\n**Yes with constraint:**\n- After 3 works, before that I'm in back-to-backs.\n\n**No:**\n- Booked solid today, sorry — how about tomorrow morning?\n\n**Asking for context:**\n- Sure — anything specific so I can prep?\n\n**Best practice:**\n- Be specific with windows\n- Ask for context if useful\n- Offer alternatives if unavailable",
        "chosen": "Yep, anything after 3 works for me. Anything specific you want me to prep?"
    },

    # ============ SHORT_EXPLAIN (8) ============
    {
        "context": "short_explain",
        "prompt": "A junior dev asked me 'why do we use Docker for everything?' How do I explain in a couple of lines?",
        "rejected": "Here's a concise explanation:\n\n**Quick answer:** Consistency across environments.\n\n**Key reasons:**\n- **Reproducibility:** Same env in dev, staging, prod\n- **Isolation:** Apps don't conflict with each other\n- **Portability:** Runs the same anywhere\n- **Speed:** Faster than VMs\n\n**Trade-offs:**\n- Learning curve\n- Some overhead vs. bare metal\n\n**Verdict:** The consistency benefit outweighs the complexity for us.",
        "chosen": "Mostly because it kills the 'works on my machine' problem. Whatever runs in your container will run the same way in staging and production — same OS libraries, same Python version, everything. The alternative is a long history of weird environment-specific bugs that take forever to track down."
    },
    {
        "context": "short_explain",
        "prompt": "Someone asked why our team picked React over Vue when we started. Quick explanation?",
        "rejected": "Here's a brief explanation:\n\n**Top reasons:**\n- **Talent pool:** Easier to hire React devs\n- **Ecosystem:** Bigger library/tool ecosystem\n- **Long-term bet:** Stronger industry momentum\n- **Team familiarity:** Most of us came from React backgrounds\n\n**Trade-offs:**\n- Vue is arguably easier to learn\n- Less boilerplate for small apps\n\n**Verdict:** React won on practical hiring + ecosystem.",
        "chosen": "Honestly mostly hiring. There are way more React developers out there than Vue developers, and we knew we'd be growing the team. The ecosystem is bigger too, so we rarely have to build something from scratch. Vue would have been fine — it just felt like a riskier long-term bet."
    },
    {
        "context": "short_explain",
        "prompt": "A new joiner asked why our standups are async on Slack instead of live. How do I explain?",
        "rejected": "Here's the rationale:\n\n**Why async:**\n- **Distributed team:** Time zones make sync hard\n- **Focus time:** Avoids breaking up morning deep work\n- **Documentation:** Written updates are searchable\n- **Quality:** People think more before writing\n\n**Trade-offs:**\n- Less face time\n- Slower back-and-forth\n- Easier to skip\n\n**Mitigation:**\n- Weekly live sync\n- 1:1s for deeper convos",
        "chosen": "Mostly because we're spread across time zones, so a live standup would mean someone is always joining at an awkward hour. Async also gives people their mornings back for focused work, and the written updates are way easier to search later. We do one live sync a week if anything needs a real conversation."
    },
    {
        "context": "short_explain",
        "prompt": "Someone asked why we use Notion instead of Confluence for our team docs. Quick explanation?",
        "rejected": "Here's the breakdown:\n\n**Why Notion:**\n- **UX:** Much better editing experience\n- **Flexibility:** Databases, kanban, docs in one tool\n- **Search:** Faster and more reliable\n- **Mobile:** Significantly better app\n\n**Why not Confluence:**\n- Clunky editor\n- Slower performance\n- Steeper learning curve\n- Aging UI\n\n**Trade-offs:**\n- Confluence integrates better with Jira\n- Confluence has better enterprise controls",
        "chosen": "Mainly because Notion is genuinely nicer to use day to day. Editing is faster, the database features cover a lot of ground we'd otherwise need separate tools for, and search actually works. Confluence has better integration with Jira if that matters to you — for us it didn't enough to outweigh the rest."
    },
    {
        "context": "short_explain",
        "prompt": "A new dev asked why they can't push directly to main. How do I explain in a couple of lines?",
        "rejected": "Here's the reasoning:\n\n**Why we block direct pushes:**\n- **Code review:** Every change gets a second pair of eyes\n- **CI safety:** Tests must pass before merge\n- **History:** PRs create discussion artifacts\n- **Mistakes:** Prevents accidental force-pushes or bad merges\n\n**The workflow:**\n1. Branch\n2. PR\n3. Review\n4. CI\n5. Merge\n\n**Trade-offs:**\n- Slightly slower for hotfixes\n- More ritual for tiny changes",
        "chosen": "Mostly to make sure every change goes through review and CI before it lands. It's saved us from broken builds and bad merges more times than I can count. There's a slight overhead for tiny fixes, but the safety net is worth it — and there's an emergency override if something is actually on fire."
    },
    {
        "context": "short_explain",
        "prompt": "Coworker asked why we use feature flags for everything. Explain in a couple lines.",
        "rejected": "Here's the rationale:\n\n**Why feature flags:**\n- **Decouple deploy from release:** Ship code without exposing features\n- **Gradual rollout:** Test with small % of users first\n- **Quick rollback:** Toggle off without redeploying\n- **A/B testing:** Compare variations\n\n**Trade-offs:**\n- Adds complexity\n- Flags pile up if not cleaned up\n- Testing matrix grows\n\n**Best practice:**\n- Remove old flags promptly\n- Document each flag's purpose",
        "chosen": "Mostly so we can ship code without immediately exposing it to users. Lets us roll out gradually, run experiments, and turn things off instantly if they break — without having to do an emergency deploy. The only catch is keeping the flag list clean; old ones tend to pile up if you're not careful."
    },
    {
        "context": "short_explain",
        "prompt": "A junior dev asked why we use Tailwind instead of writing regular CSS. Quick explanation?",
        "rejected": "Here's the breakdown:\n\n**Why Tailwind:**\n- **Speed:** Build UI faster without naming classes\n- **Consistency:** Design tokens baked in\n- **Co-location:** Styles next to markup\n- **Tree-shaking:** Only ships used utilities\n\n**Common objections:**\n- 'Cluttered markup' — manageable with extracted components\n- 'Re-learning' — only takes a week or two\n- 'Lock-in' — utilities are easy to convert back\n\n**Verdict:** Speed and consistency win for us.",
        "chosen": "Mainly speed and consistency. You stop spending mental energy naming classes and worrying about specificity, and the design tokens are baked in so spacing and colors stay consistent across the app without anyone enforcing it. The markup looks busier at first but you stop noticing it pretty quickly."
    },
    {
        "context": "short_explain",
        "prompt": "Coworker asked why we deploy twice a week instead of continuously. How do I explain?",
        "rejected": "Here's the reasoning:\n\n**Why twice-weekly:**\n- **Stability:** Reduces noise in production metrics\n- **Coordination:** Easier to align team/communication\n- **Risk:** Lower blast radius for any single deploy\n- **Reviews:** Forces batch review of changes\n\n**Why not continuous:**\n- Our infra doesn't fully support yet\n- Team prefers predictable cadence\n- Customer comms tied to deploy windows\n\n**Trade-offs:**\n- Slower change delivery\n- Larger PRs at deploy time",
        "chosen": "A few reasons — our infrastructure isn't quite set up for continuous deploys, our customer comms team needs predictable windows to coordinate around, and honestly, twice a week makes it easier to spot what changed when something breaks. We'll probably move to more frequent deploys once a couple of these things get fixed."
    },

    # ============ DIVERSITY BALLAST (2) ============
    {
        "context": "narrative",
        "prompt": "Tell me about a memory from when you were eight years old.",
        "rejected": "A memory from age 8 — details:\n\n**Setting:** Summer afternoon\n**Location:** Grandparents' backyard\n\n**Activity:**\n- Building a fort from old blankets\n- Sister and cousins involved\n- Snacks brought out by grandma\n\n**Sensory details:**\n- Smell of cut grass\n- Sound of sprinkler\n- Warm sun on skin\n\n**Significance:**\n- Pure, unhurried play\n- Felt safe and loved\n- Has stayed vivid for decades",
        "chosen": "There's an afternoon at my grandparents' house I keep coming back to — I would have been eight, maybe nine. My cousins and I had dragged every blanket we could find out into the backyard and were building a fort under the cherry tree. My grandmother kept appearing every twenty minutes with snacks none of us had asked for and pretending not to notice when we ate them. The sprinkler was going somewhere in the yard. I remember thinking, in a vague eight-year-old way, that I would always remember this. And I have."
    },
    {
        "context": "explanatory",
        "prompt": "Briefly explain why the first number in a negotiation matters so much.",
        "rejected": "Why the first number matters — explained:\n\n**Concept:** Anchoring bias\n\n**Mechanism:**\n- First number sets reference point\n- Subsequent discussion adjusts around it\n- People underweight info that contradicts the anchor\n\n**Research:**\n- Kahneman & Tversky (1974) — original anchoring studies\n- Replicated across decades\n- Holds even when anchor is clearly arbitrary\n\n**Practical implications:**\n- Speak first if confident in your number\n- Counter-anchor immediately if anchored against\n- Be aware in salary negotiations",
        "chosen": "Because the first number that gets said becomes the gravitational center of the whole conversation, even when everyone knows it's negotiable. Whatever range you discuss after that will quietly cluster around it. There are well-known psychology studies — the original work from Kahneman and Tversky — where people anchored on completely random numbers and still drifted toward them in their final answers. So if you have a strong number, say it first. And if someone anchors you with theirs, push back fast."
    },
]


def main() -> None:
    path = Path("data/formatting_pairs_v1.jsonl")
    assert path.exists(), f"Expected dataset at {path}"

    # Sanity check: confirm no duplicate prompts vs. existing file
    existing_prompts = set()
    with path.open() as f:
        for line in f:
            existing_prompts.add(json.loads(line)["prompt"])

    new_unique = [r for r in ROWS if r["prompt"] not in existing_prompts]
    skipped = len(ROWS) - len(new_unique)

    with path.open("a") as f:
        for row in new_unique:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Final stats
    counts = Counter()
    register_counts = Counter()
    with path.open() as f:
        all_rows = [json.loads(line) for line in f]
    for r in all_rows:
        counts[r["context"]] += 1
        if "register" in r:
            register_counts[r["register"]] += 1

    print(f"Appended: {len(new_unique)} new rows (skipped {skipped} duplicates)")
    print(f"Total rows: {len(all_rows)}")
    print("\nBy context:")
    for c, n in sorted(counts.items()):
        print(f"  {c:18} {n}")
    print("\nBy email register:")
    for r, n in sorted(register_counts.items()):
        print(f"  {r:20} {n}")


if __name__ == "__main__":
    main()
