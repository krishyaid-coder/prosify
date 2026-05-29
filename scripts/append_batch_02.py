"""
Batch 2 append script — adds 50 more use-case-focused DPO pairs.
Topics all distinct from batch 1. Failure modes deliberately varied.
"""

import json
from pathlib import Path
from collections import Counter

ROWS = [
    # ============ EMAIL_DRAFT (15) ============
    # --- indian_corporate (5) ---
    {
        "context": "email_draft", "register": "indian_corporate",
        "prompt": "Email finance team member Anita requesting reimbursement for last week's client visit travel — flights, hotel, and meals. Total around 25,000.",
        "rejected": "Subject: Request for Travel Reimbursement — Client Visit\n\nDear Anita,\n\nGreetings! I hope you are doing well. I would like to submit a travel reimbursement claim for last week's client visit.\n\n**Trip details:**\n1. Purpose: Client visit\n2. Duration: Last week\n3. Total claim: ~₹25,000\n\n**Expense breakdown:**\n| Category | Amount |\n|----------|--------|\n| Flights  | ~₹15,000 |\n| Hotel    | ~₹7,000  |\n| Meals    | ~₹3,000  |\n\n**Attached documents:**\n- All original receipts\n- Boarding passes\n- Trip approval email\n\nKindly process the same and revert in case any additional documentation is required.\n\nThanks and regards,\n[Your Name]",
        "chosen": "Subject: Travel reimbursement — client visit last week\n\nHi Anita,\n\nI'd like to claim reimbursement for last week's client visit — flights, hotel, and meals come to about ₹25,000 total. I've attached all the receipts along with the original trip approval. Let me know if you need anything else from my side.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "indian_corporate",
        "prompt": "Email my manager Manoj — my mother has been hospitalized and I need to fly home today. I'll be on email when I can.",
        "rejected": "Subject: Urgent Personal Leave Required — Family Medical Emergency\n\nDear Manoj,\n\nI hope this email reaches you immediately. I am writing to inform you of an urgent personal situation:\n\n**Situation:**\n- Mother has been hospitalized\n- Travelling home immediately\n- Departure: Today\n\n**Expected duration:** Uncertain at this time\n\n**Work-related notes:**\n1. Critical handovers to be communicated separately\n2. Will be reachable on email intermittently\n3. Phone may be unavailable during travel\n4. Will provide updates as situation evolves\n\nApologies for the short notice. I will keep you informed.\n\nWith regards,\n[Your Name]",
        "chosen": "Subject: Family emergency — need to travel home today\n\nHi Manoj,\n\nMy mother has been hospitalized and I need to fly home today. I'm not sure yet how long I'll be away. I'll try to send a proper handover note before I leave, and I'll be on email when I can — but please assume I'll be slow to respond for the next few days.\n\nWill keep you updated.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "indian_corporate",
        "prompt": "Email my former manager Sandeep asking if he'd write a letter of recommendation for me — I'm applying to a master's program in October.",
        "rejected": "Subject: Request for Letter of Recommendation — Master's Program Application\n\nDear Sandeep Sir,\n\nI hope you are doing well. I am writing with an important request.\n\n**Background:**\n- I am applying for a Master's program\n- Application deadline: October\n- Three letters of recommendation required\n\n**Request:**\n- Would you be willing to write one of my letters?\n- Your perspective on my work would be invaluable\n\n**Documents I can share to help:**\n1. CV / Resume\n2. Statement of purpose draft\n3. Program details\n4. My key contributions while reporting to you\n\n**Timeline:**\n- I can share materials this week\n- Letter would be needed by: late September\n\nThank you in advance for considering. Looking forward to your response.\n\nWith regards,\n[Your Name]",
        "chosen": "Subject: Would you be willing to write me a recommendation letter?\n\nHi Sandeep,\n\nI'm applying to a master's program in October and was hoping you might be willing to write me a letter of recommendation. Working with you was easily the most formative part of my early career, and a letter from you would really matter.\n\nIf you're up for it, I can send over my CV, statement of purpose, and a quick note on what to highlight. The letter would need to be in by late September.\n\nNo pressure if it's not workable — I know you're busy.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "indian_corporate",
        "prompt": "Email senior management (Mr. Sharma) proposing a one-day team offsite next month — informal, focused on team bonding after a stressful quarter.",
        "rejected": "Subject: Proposal — One-Day Team Offsite\n\nDear Mr. Sharma,\n\nI hope you are doing well. I would like to formally propose a one-day team offsite for next month.\n\n**Rationale:**\n1. Team has been through a stressful quarter\n2. Strong need for informal bonding\n3. Will help recharge before next quarter\n\n**Proposed format:**\n- **Duration:** One day\n- **Style:** Informal, no agenda-heavy sessions\n- **Focus:** Team bonding, light activities\n\n**Logistics (high-level):**\n- Venue: Within city, indoor + outdoor\n- Budget: To be estimated based on approval\n- Date: Flexible, ideally mid-month\n\n**Next steps:**\n- Your in-principle approval\n- Detailed plan and budget to follow\n- Coordination with HR\n\nKindly let me know your thoughts. Happy to discuss further.\n\nWith regards,\n[Your Name]",
        "chosen": "Subject: Proposing a one-day team offsite next month\n\nDear Mr. Sharma,\n\nAfter the quarter we've just had, I'd like to propose a one-day team offsite next month — something informal, focused on bonding rather than work sessions. The team needs a real exhale before the next push, and I think a low-key day out together would do more for morale than any number of internal meetings.\n\nIf you're open to it in principle, I'll put together a proper plan with venue options and a budget estimate.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "indian_corporate",
        "prompt": "Apology email to Lakshmi, my skip-level manager, for sending wrong numbers in yesterday's client presentation. I've already corrected and resent.",
        "rejected": "Subject: Apology — Incorrect Figures in Yesterday's Client Presentation\n\nDear Lakshmi,\n\nI am writing to formally apologize for an error in yesterday's client presentation.\n\n**The error:**\n- Incorrect figures were presented to the client\n- Issue identified post-presentation\n- Could have impacted client perception\n\n**Corrective actions already taken:**\n1. Corrected version sent to the client\n2. Client has acknowledged receipt\n3. Internal team has been notified\n\n**Root cause:**\n- Used outdated data source\n- Did not cross-check before finalizing\n- Failure of review process on my end\n\n**Preventive measures going forward:**\n- Mandatory peer review for client-facing data\n- Triple-check data sources\n- Build review buffer into timelines\n\nI take full responsibility and assure you this will not be repeated.\n\nApologies once again,\n[Your Name]",
        "chosen": "Subject: Apology — wrong figures in yesterday's client presentation\n\nHi Lakshmi,\n\nI owe you an apology. The figures in yesterday's client deck were wrong — I'd pulled from an outdated source and didn't double-check before finalizing. I've sent the corrected version to the client this morning and they've acknowledged it.\n\nI'm setting up a peer-review step for any client-facing numbers going forward so this doesn't happen again. Happy to walk you through what changed if it would help.\n\nThanks,\n[Your Name]"
    },
    # --- us_tech_casual (5) ---
    {
        "context": "email_draft", "register": "us_tech_casual",
        "prompt": "Email team lead Chris asking him to help unblock a stalled code review — it's been sitting for 5 days and is blocking the release.",
        "rejected": "Subject: Stalled Code Review Blocking Release\n\nHi Chris,\n\nNeed your help on a stalled review:\n\n**Issue:**\n- PR sitting 5 days without review\n- Blocks upcoming release\n- Other work is dependent\n\n**PR details:**\n- Link: [PR URL]\n- Size: [LOC]\n- Reviewer: [name]\n\n**Asks:**\n- Nudge the reviewer, or\n- Assign someone else, or\n- Review yourself if quick\n\n**Impact if not unblocked:**\n- Release slips by at least 2 days\n- Customer commitment at risk\n- Engineering credibility takes a hit\n\nLet me know how you'd like to handle.\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Need help unblocking a code review — release is at risk\n\nHey Chris,\n\nMy PR [link] has been sitting for review for five days and it's blocking the release. The current reviewer is heads down on something else. Could you either nudge them, reassign it, or take a pass yourself? It's not a huge change.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "us_tech_casual",
        "prompt": "Quick email to IT (Tina) — my new laptop was supposed to arrive last Friday and hasn't. Trying not to be annoying but I'm on my old machine which barely runs the build.",
        "rejected": "Subject: Status Check — New Laptop Delivery\n\nHi Tina,\n\nFollowing up on my pending laptop:\n\n**Status:**\n- Expected delivery: Last Friday\n- Current status: Not received\n- Days delayed: 3+ working days\n\n**Why I'm following up:**\n- Old laptop barely runs builds\n- Productivity impact\n- Need ETA to plan workarounds\n\n**Asks:**\n- Confirm shipment status\n- Provide updated ETA\n- Suggest temporary alternative if delayed further\n\nAppreciate any update!\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Any update on my new laptop?\n\nHi Tina,\n\nNot trying to be annoying about this — but my new laptop was supposed to arrive last Friday and hasn't shown up. I'm scraping by on my old machine but it barely runs the build at this point. Any chance you could check on the shipment and let me know an ETA?\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "us_tech_casual",
        "prompt": "Email my team welcoming Jamie, our new intern who starts Monday. Make it warm but brief.",
        "rejected": "Subject: Welcome Jamie — New Intern Starting Monday\n\nHi team,\n\nExcited to welcome a new face to the team!\n\n**Who:** Jamie\n**Role:** Intern\n**Start date:** Monday\n\n**A bit about Jamie:**\n- Background: [TBD]\n- Will rotate through: [areas]\n- Mentor: [name]\n\n**How you can help:**\n- 👋 Say hi when you see them\n- 🤝 Be patient with onboarding questions\n- ☕ Grab a coffee with them in week 1\n- 📚 Share helpful docs/links\n\n**First week:**\n- 1:1s with team members\n- Tooling setup\n- First task assigned by EOW\n\nLet's make Jamie feel at home!\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Jamie joins as our intern on Monday\n\nHi all,\n\nJamie is starting with us on Monday as our new intern. They'll be rotating around different parts of the team over the first few weeks. Please be welcoming, jump on a coffee with them if you can in their first week, and be patient with the onboarding questions — we've all been there.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "us_tech_casual",
        "prompt": "Email Drew proposing we cancel the recurring 'product sync' on Wednesdays — it's been empty of useful content for weeks and people are tuning out.",
        "rejected": "Subject: Proposing We Cancel the Wednesday Product Sync\n\nHi Drew,\n\nWant to float an idea about the Wednesday product sync:\n\n**Observation:**\n- Meeting has been low-value for weeks\n- Same updates repeated\n- People visibly checked out\n\n**Proposal:**\n- ❌ Cancel the recurring meeting\n- ✅ Replace with async Slack thread (weekly)\n- ✅ Schedule ad-hoc only when needed\n\n**Benefits:**\n- 5 people × 30 min = 2.5 hours/week saved\n- Less context switching\n- Better attendance when meetings DO happen\n\n**Risks:**\n- Less informal team time → mitigate with monthly social\n- Some prefer real-time → offer optional weekly office hours\n\nWhat do you think?\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Should we kill the Wednesday product sync?\n\nHey Drew,\n\nBeen thinking — the Wednesday product sync hasn't really delivered much for a few weeks now. Most of what gets said could've been a Slack thread, and people are pretty visibly tuning out. Want to just cancel the recurring and only schedule it when there's actually something to discuss?\n\nHappy to hear it if you think there's value I'm missing.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "us_tech_casual",
        "prompt": "Email my manager Pat asking for clearer context on this week's new project assignment — the requirements doc was thin and I want to be sure I'm building the right thing.",
        "rejected": "Subject: Clarification Needed — New Project Requirements\n\nHi Pat,\n\nWanted to flag some questions on the new project:\n\n**My read of the requirements:**\n- Build [X]\n- For [audience]\n- By [deadline]\n\n**Where I need clarity:**\n1. **Success criteria:** What does 'done' look like?\n2. **Scope:** Hard 'no's vs. nice-to-haves?\n3. **Dependencies:** Who else is involved?\n4. **Constraints:** Any tech, budget, or timing limits I should know?\n\n**Suggested path forward:**\n- 30-min sync to align\n- I draft a one-pager, you review\n- Then I start building\n\nWant to make sure I don't burn cycles on the wrong thing.\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Quick sync on the new project requirements?\n\nHi Pat,\n\nI started digging into the new project and the requirements doc is a bit thinner than I'd like — I have some questions about scope and what 'done' actually looks like before I commit to a direction. Could we do a quick 30 minutes this week to align? I'd rather spend that time up front than build the wrong thing.\n\nThanks,\n[Your Name]"
    },
    # --- global_neutral (5) ---
    {
        "context": "email_draft", "register": "global_neutral",
        "prompt": "Email a contractor asking them for a revised timeline — original delivery date was last week and we haven't received an update.",
        "rejected": "Subject: Request for Revised Timeline — Pending Delivery\n\nDear [Contractor],\n\nI hope you are well. I am writing regarding the project deliverable that was due last week.\n\n**Current status:**\n- Original deadline: Last week\n- Status: Not yet received\n- Last communication: [date]\n\n**What we need:**\n1. Revised, realistic delivery date\n2. Reason for the delay\n3. Confirmation that quality will be maintained\n\n**Why this matters:**\n- Our internal milestones depend on this\n- Stakeholders are awaiting updates\n- Knock-on impact on downstream work\n\nKindly send a written update by end of day tomorrow so we can plan accordingly.\n\nBest regards,\n[Your Name]",
        "chosen": "Subject: Could you send a revised timeline?\n\nHi [Name],\n\nThe original delivery date for the project was last week and we haven't received an update since. Could you send over a revised timeline by end of day tomorrow, along with a brief note on what caused the slip? We have downstream work waiting on this, so the sooner we have a realistic date the better we can plan around it.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "global_neutral",
        "prompt": "Email to all customers announcing a 4-hour scheduled maintenance window this Saturday night — they should expect intermittent service interruptions.",
        "rejected": "Subject: Scheduled Maintenance — Saturday Night\n\nDear Valued Customer,\n\nWe are writing to inform you of upcoming scheduled maintenance on our platform.\n\n**Maintenance window:**\n- **Date:** This Saturday\n- **Time:** [Start time] - [End time] (4 hours)\n- **Timezone:** [Specify]\n\n**What to expect:**\n- ⚠️ Intermittent service interruptions\n- ⚠️ Possible delays in transactions\n- ⚠️ Some features may be temporarily unavailable\n\n**What we are doing:**\n- Critical infrastructure upgrades\n- Security patches\n- Performance improvements\n\n**Recommended actions for you:**\n1. Complete urgent tasks before the window\n2. Avoid initiating large operations during the window\n3. Contact support if issues persist after the window\n\nThank you for your patience as we work to improve your experience.\n\nSincerely,\nThe [Company] Team",
        "chosen": "Subject: Scheduled maintenance this Saturday night (4 hours)\n\nHi,\n\nWe'll be performing scheduled maintenance this Saturday from [start] to [end] [timezone]. During that window you may see intermittent interruptions and some features may be briefly unavailable.\n\nIf you have anything time-sensitive, we'd recommend wrapping it up before the window starts. Service should be back to normal as soon as the maintenance completes.\n\nThanks for your patience,\nThe [Company] Team"
    },
    {
        "context": "email_draft", "register": "global_neutral",
        "prompt": "Email a former colleague (Hiroshi) I haven't spoken to in a year — I'd like his career advice as I'm considering a switch from engineering management back to IC.",
        "rejected": "Subject: Catching Up — Career Advice Request\n\nHi Hiroshi,\n\nI hope this email finds you well. It has been about a year since we last spoke and I would love to reconnect.\n\n**Where I am:**\n- Currently in engineering management\n- Considering switching back to individual contributor\n- Wrestling with the decision for a few months\n\n**Why I'm reaching out:**\n- You made a similar transition\n- Value your perspective\n- Would love to hear what helped/hurt your decision\n\n**Ask:**\n- 30-45 minute call in the next few weeks?\n- Coffee if you're nearby?\n- Async over email also works\n\n**On my end:**\n- Flexible on timing\n- Happy to share more context\n- Looking forward to catching up\n\nThanks in advance!\n\nBest,\n[Your Name]",
        "chosen": "Subject: Long time — could I pick your brain about something?\n\nHi Hiroshi,\n\nIt's been about a year — hope life and work are treating you well. I'm reaching out because I'm wrestling with a decision and I think you're one of the few people I know who'd have useful perspective: I'm considering moving back from engineering management to IC, and I remember you made a similar transition.\n\nAny chance you'd have 30 minutes for a call in the next few weeks? Coffee works too if you're around. And if it's easier, I'm happy to ask the actual questions over email.\n\nWould be good to catch up either way.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "global_neutral",
        "prompt": "Reply to an angry customer email — they said our product has been broken for three days and nobody is responding. Acknowledge the issue, take responsibility, give a real next step.",
        "rejected": "Subject: Re: Issue with Your Service — Sincere Apologies\n\nDear [Customer],\n\nThank you for taking the time to write to us, and we sincerely apologize for the experience you've had.\n\n**We acknowledge:**\n- Service issues have been ongoing for 3 days\n- Our response time has been unacceptable\n- This has caused you frustration and disruption\n\n**Taking responsibility:**\n1. We dropped the ball on responsiveness\n2. The product issue should have been escalated faster\n3. Your account deserved better\n\n**What we are doing immediately:**\n- ✅ Engineering has been pulled in to investigate\n- ✅ A dedicated point of contact has been assigned (me)\n- ✅ Updates every 4 hours until resolution\n- ✅ Service credit will be issued post-resolution\n\n**Timeline:**\n- Investigation: Within next 2 hours\n- Initial diagnosis: By end of day\n- Resolution target: 24-48 hours\n\nWe truly value your business and are committed to making this right.\n\nWith apologies,\n[Your Name]",
        "chosen": "Subject: Re: your issue — apologies and what we're doing\n\nHi [Name],\n\nYou're right to be frustrated, and I'm sorry. Three days of a broken product with no response from us isn't acceptable, and I take responsibility for the silence.\n\nHere's what's happening now: I've pulled engineering in to investigate as a priority, and I'll be your direct point of contact until this is resolved. You'll hear from me with an update every four hours, even if there's nothing new to report. We'll also issue a service credit once we're back to normal.\n\nIf there's anything specific you need from us in the meantime, please reply directly to this email.\n\nApologies again,\n[Your Name]"
    },
    {
        "context": "email_draft", "register": "global_neutral",
        "prompt": "Email a partner organization proposing an alternative to their original collaboration idea — we can't do what they suggested due to compliance, but we could do something simpler that still gets to their goal.",
        "rejected": "Subject: Re: Collaboration Proposal — Alternative Approach\n\nDear [Partner],\n\nThank you for sharing the collaboration proposal. After reviewing internally, I wanted to share where we landed.\n\n**Original proposal:**\n- [Brief restate]\n- Identified blocker: Compliance constraints on our side\n\n**Why we cannot proceed as-is:**\n1. Regulatory framework prohibits [X]\n2. Risk threshold exceeded\n3. Legal team has flagged concerns\n\n**Alternative we can offer:**\n- ✅ Simpler structure that avoids the compliance issue\n- ✅ Still addresses your underlying goal\n- ✅ Faster to execute\n- ✅ Lower overhead for both teams\n\n**High-level shape of alternative:**\n- [Component 1]\n- [Component 2]\n- [Component 3]\n\n**Proposed next steps:**\n1. 30-minute call to discuss\n2. Draft MOU within 2 weeks\n3. Kick off within the month\n\nLet me know if this direction works.\n\nBest regards,\n[Your Name]",
        "chosen": "Subject: Re: collaboration — proposing a simpler alternative\n\nHi [Name],\n\nThanks for the collaboration proposal. Unfortunately, the original shape of it runs into compliance constraints on our side that we can't get around — but I don't want to leave it there, because I think we can still get to what you're actually trying to achieve.\n\nA simpler structure would work for us and should still hit your underlying goal. It would also be faster to put in place and lower overhead for both sides. Could we set up a 30-minute call this week to walk through it?\n\nThanks,\n[Your Name]"
    },

    # ============ EMAIL_REFINE (15) ============
    # --- indian_corporate (5) ---
    {
        "context": "email_refine", "register": "indian_corporate",
        "prompt": "Polish this resignation acceptance reply — it sounds stilted: 'Dear Sir, I have received your resignation letter and the same is hereby accepted. Your last working day will be as per the notice period. We will initiate the exit formalities. Regards.'",
        "rejected": "Here's a warmer, more human version:\n\n**Subject:** Re: Resignation — Acceptance and Next Steps\n\n**Body:**\n\nDear [Name],\n\nThank you for your resignation letter, which I've accepted.\n\n**Next steps:**\n1. Last working day: Per notice period\n2. HR will reach out for exit formalities\n3. Knowledge transfer plan: To be discussed\n4. Final settlement: Standard timeline\n\n**On a personal note:**\n- Thank you for your contributions\n- Wishing you the best\n- Always welcome to stay in touch\n\nBest wishes,\n[Your Name]\n\n**Improvements:**\n- Removed bureaucratic phrasing\n- Added warmth\n- Maintained professional structure",
        "chosen": "Subject: Re: your resignation\n\nDear [Name],\n\nThank you for the note — I've accepted your resignation, with your last working day per the notice period. HR will be in touch shortly to walk you through the formalities.\n\nI'm sorry to see you go. You've been a real part of this team, and you'll be missed. Let's find time in your last few weeks for a proper conversation — and please do stay in touch.\n\nWishing you the best,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "indian_corporate",
        "prompt": "Refine this — it sounds too pleading: 'Dear Sir, This is regarding my pending leave application which I submitted last week. I really really need this leave for my sister's wedding and I would be very very grateful if you could approve it as soon as possible. Please sir, please consider.'",
        "rejected": "Here's a more professional follow-up:\n\n**Subject:** Follow-up — Leave Application for Sister's Wedding\n\n**Body:**\n\nDear [Name],\n\nGentle reminder on my pending leave application:\n\n**Application details:**\n- Submitted: Last week\n- Reason: Sister's wedding\n- Dates requested: [insert]\n- Approval pending\n\n**Why I'm following up:**\n- Travel and event preparation requires advance planning\n- Family commitments cannot be rescheduled\n- Would appreciate confirmation either way\n\n**What I can offer:**\n- Detailed handover before leave\n- Availability on email for urgent matters\n- Coverage by [colleague name]\n\nKindly let me know.\n\nThanks,\n[Your Name]\n\n**What changed:**\n- Removed pleading tone\n- Stated facts clearly\n- Added professional reasoning",
        "chosen": "Subject: Follow-up on my leave application from last week\n\nDear [Name],\n\nFollowing up on the leave application I submitted last week for my sister's wedding. Could you let me know either way at your convenience? I need to start booking travel, and the rest of the family is waiting on me to confirm.\n\nHappy to walk you through my handover plan before I go.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "indian_corporate",
        "prompt": "Polish this self-evaluation for my annual appraisal — it sounds too modest and won't help me: 'Sir, I have tried my best this year. I worked on a few projects and I think I did okay. I am still learning and have a lot to improve. I am grateful for the opportunity.'",
        "rejected": "Here's a stronger, more confident version:\n\n**Subject:** Self-Evaluation — [Your Name], FY[X]\n\n**Body:**\n\nDear [Manager],\n\nSubmitting my self-evaluation for the year:\n\n**Key contributions:**\n1. **[Project 1]:** Delivered [outcome]\n2. **[Project 2]:** Led [scope], achieved [result]\n3. **[Project 3]:** Drove [initiative], with [impact]\n\n**Skills strengthened:**\n- Technical: [areas]\n- Leadership: [areas]\n- Collaboration: [examples]\n\n**Areas for growth:**\n- [Honest area 1] — plan: [steps]\n- [Honest area 2] — plan: [steps]\n\n**Career goals for next year:**\n- [Goal 1]\n- [Goal 2]\n- [Goal 3]\n\nLooking forward to discussing in our review.\n\nThanks,\n[Your Name]\n\n**Improvements:**\n- Specific over vague\n- Confident over modest\n- Forward-looking growth areas",
        "chosen": "Subject: Self-evaluation — [Your Name], FY[X]\n\nDear [Manager],\n\nA quick self-evaluation for this year. I led the work on [Project 1], which delivered [specific outcome], and contributed meaningfully to [Project 2] and [Project 3]. I'd particularly highlight [one concrete win that took initiative], because it's the kind of work I'd like to take on more of next year.\n\nThe areas I most want to grow in are [Area 1] and [Area 2] — for [Area 1] I'm planning to [specific step], and for [Area 2] I'd value your input on the right next move.\n\nLooking forward to discussing in our review.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "indian_corporate",
        "prompt": "Tone this down — sounds too over-the-top: 'Dear Sir, I cannot thank you enough for the wonderful appraisal feedback. Your kind words mean the world to me and I am deeply moved. I promise to work even harder and not let you down. Thanking you from the bottom of my heart.'",
        "rejected": "Here's a more measured, professional version:\n\n**Subject:** Thank You — Appraisal Feedback\n\n**Body:**\n\nDear [Manager],\n\nThank you for the thoughtful appraisal feedback today.\n\n**What stood out for me:**\n- Your specific recognition of [area]\n- Honest input on [growth area]\n- Clear direction for the year ahead\n\n**My commitments coming out of this:**\n- Continue strong performance on [area]\n- Focus on growth in [area]\n- Apply your suggestions actively\n\n**Looking ahead:**\n- Excited about the year ahead\n- Will check in regularly on progress\n- Available for any further discussion\n\nThanks again,\n[Your Name]\n\n**Improvements:**\n- Reduced over-effusive language\n- Specific and forward-looking\n- Professional but warm",
        "chosen": "Subject: Thank you for the appraisal feedback\n\nDear [Manager],\n\nThank you for the thoughtful feedback today. It means a lot, and the specifics you called out — particularly on [area] — really resonated. I've also taken your input on growth areas to heart and will come back next quarter with concrete progress to share.\n\nThanks again,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "indian_corporate",
        "prompt": "Refine this circular email — it's a simple reminder but sounds like a legal notice: 'Dear All, This is to remind all employees that as per company policy, all official communication must be done through official email IDs only. Personal email IDs must not be used under any circumstances. Strict compliance is expected. Regards.'",
        "rejected": "Here's a friendlier version that still gets the policy across:\n\n**Subject:** Reminder — Use Official Email for All Work Communication\n\n**Body:**\n\nHi team,\n\nQuick reminder on email usage:\n\n**The policy:**\n- ✅ Use official email IDs for all work communication\n- ❌ Avoid personal email IDs for anything work-related\n\n**Why it matters:**\n- Data security\n- Compliance and audit trail\n- IP protection\n\n**Action needed:**\n- Audit your own usage\n- Update any cross-team threads accordingly\n- Reach out if you spot edge cases\n\n**Questions?**\n- Drop me a line, happy to clarify\n\nThanks,\n[Your Name]\n\n**Improvements:**\n- Removed legal-style phrasing\n- Conversational tone\n- Clear ask",
        "chosen": "Subject: Quick reminder — please use your official email for work communication\n\nHi team,\n\nJust a quick reminder — please make sure all work-related communication goes through your official company email, not your personal one. It's mostly about keeping things on the record for security and audit purposes. If you've been using a personal address for any ongoing threads, please move them over.\n\nLet me know if anything is unclear.\n\nThanks,\n[Your Name]"
    },
    # --- us_tech_casual (5) ---
    {
        "context": "email_refine", "register": "us_tech_casual",
        "prompt": "Polish this — I drafted it while panicking and it shows: 'OK so we have a major outage right now. Payments are down. I think it started 20 min ago. I dont know root cause yet. I'm pulling everyone in. We need to figure out a comms plan asap. Will update soon.'",
        "rejected": "Here's a more composed version:\n\n**Subject:** 🚨 Active Outage — Payments Down\n\n**Body:**\n\nHi team,\n\nKicking off an incident:\n\n**Status:**\n- 🔴 Payments: DOWN\n- Started: ~20 minutes ago\n- Root cause: Under investigation\n\n**Response in progress:**\n- All engineers being pulled in\n- War room: [link]\n- Incident commander: [name]\n\n**Comms plan (next 30 minutes):**\n- Internal: This thread, updates every 15 min\n- External: Status page + customer email TBD\n- Leadership: Will brief separately\n\n**Next update:** 15 minutes\n\n[Your Name]",
        "chosen": "Subject: Active outage — payments down (started ~20 min ago)\n\nHi team,\n\nWe have a live outage — payments have been down since about 20 minutes ago. Root cause is still unclear. I'm pulling the on-call engineers into a war room now, and I'll have [name] act as incident commander.\n\nWe need a comms plan within the next 30 minutes: internal status update cadence, status page, and a customer-facing email. I'll send the first proper update in 15 minutes regardless of progress.\n\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "us_tech_casual",
        "prompt": "Polish this push-back on scope creep — sounds too hesitant: 'Hey, so I was just wondering if maybe we could perhaps revisit the scope a little bit? It feels like things have been growing kind of a lot and I'm not sure we can hit the deadline. Just a thought, totally open to your thinking!'",
        "rejected": "Here's a firmer but professional version:\n\n**Subject:** Scope Concern — Need to Revisit\n\n**Body:**\n\nHi [Name],\n\nWanted to flag a real concern on scope:\n\n**What's happening:**\n- Scope has grown significantly since kickoff\n- Original deadline assumed smaller scope\n- Team capacity unchanged\n\n**The math:**\n- Original estimate: [X weeks]\n- Current scope estimate: [Y weeks]\n- Available time: [Z weeks]\n- Gap: [Y-Z weeks]\n\n**Options:**\n1. Hold scope, push deadline\n2. Hold deadline, cut scope\n3. Add resources (unlikely?)\n\n**My recommendation:**\n- Option 2 — let's identify what to cut\n- Happy to draft a proposed cut list\n\nLet's discuss this week.\n\nThanks,\n[Your Name]\n\n**Improvements:**\n- Removed hedging\n- Quantified concern\n- Offered concrete options",
        "chosen": "Subject: We need to revisit scope or push the deadline\n\nHi [Name],\n\nI need to flag this honestly — scope has grown enough since kickoff that I don't think we can hit the original deadline. We essentially have three options: push the date, cut scope to fit, or add people. My read is the cleanest path is to cut scope. I can put together a proposed cut list if you're open to it.\n\nCould we find time this week to align on which way to go?\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "us_tech_casual",
        "prompt": "Polish this sprint retro summary I scribbled — it's a mess: 'Hey all, so retro was good i think. We talked about a bunch of stuff. Main themes were communication issues, the sprint was too packed, and we need to fix the testing pipeline. Action items i think were: someone to look at testing, talk less in standup, and review sprint planning process. Let me know if i missed anything.'",
        "rejected": "Here's a cleaner version:\n\n**Subject:** Sprint Retro Summary — Themes & Action Items\n\n**Body:**\n\nHi all,\n\nQuick summary from today's retro:\n\n**Main themes raised:**\n1. **Communication issues** — slowing collaboration\n2. **Sprint overload** — too many commitments\n3. **Testing pipeline** — flaky, slow, painful\n\n**Action items:**\n| Item | Owner | Due |\n|------|-------|-----|\n| Audit testing pipeline | TBD | Next sprint |\n| Tighten standup format | All | Immediately |\n| Review sprint planning | Lead | Before next planning |\n\n**Owners needed:**\n- Testing pipeline audit volunteer?\n- Standup format proposal volunteer?\n\nLet me know if I missed or misrepresented anything.\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Sprint retro — themes and action items\n\nHi all,\n\nQuick recap from today's retro. Three themes came up: communication gaps that are slowing us down, sprint commitments that were too heavy, and the testing pipeline being a constant source of pain.\n\nThree action items came out of it: someone needs to own auditing the testing pipeline (volunteers welcome), we're going to tighten up standup so it's less wandering, and the lead will revisit the sprint planning process before next planning.\n\nLet me know if I missed something or got anything wrong.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "us_tech_casual",
        "prompt": "Refine these vague action items into something useful: 'Hey team, great meeting today! Next steps: someone should follow up on the design feedback, we should think more about the API approach, and lets sync again soon. Thanks!'",
        "rejected": "Here's a more actionable version:\n\n**Subject:** Action Items from Today's Meeting\n\n**Body:**\n\nHi team,\n\nThree clear action items from today's discussion:\n\n**1. Design feedback follow-up**\n- **Owner:** [Name]\n- **Due:** Friday\n- **Detail:** Consolidate feedback, share with design team\n\n**2. API approach decision**\n- **Owner:** [Name]\n- **Due:** Next Tuesday\n- **Detail:** Draft brief comparing 2-3 options with recommendation\n\n**3. Follow-up sync**\n- **Owner:** [Name]\n- **When:** Next week\n- **Goal:** Lock decisions, align on next sprint\n\nPlease confirm ownership by EOD.\n\nThanks,\n[Your Name]\n\n**Improvements:**\n- Specific owners\n- Specific dates\n- Specific deliverables",
        "chosen": "Subject: Action items from today's meeting\n\nHi team,\n\nThree concrete things from today. First, [Name] is going to consolidate the design feedback and get it to the design team by Friday. Second, [Name] will draft a short comparison of two or three API approaches with a recommendation, due Tuesday. Third, we'll meet again next week to lock decisions before sprint planning — I'll send an invite.\n\nIf I assigned anything you can't do, push back today so we can reshuffle.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "us_tech_casual",
        "prompt": "Tighten this — I'm over-thanking and it's awkward: 'Hi! Thank you SO much for the kind words about my work on the migration. Really, truly, I cannot tell you how much it means to hear that from you. Your feedback genuinely made my whole week. Thank you thank you thank you.'",
        "rejected": "Here's a more measured version:\n\n**Subject:** Thanks for the Feedback on the Migration\n\n**Body:**\n\nHi [Name],\n\nThank you for the kind words on the migration work.\n\n**What stood out:**\n- Your specific recognition of [area]\n- Coming from you, it carries weight\n- Honestly made my week\n\n**My takeaway:**\n- Will keep the same approach for upcoming projects\n- Open to more feedback as I take on similar work\n\nThanks again,\n[Your Name]\n\n**Improvements:**\n- Reduced over-thanking\n- Added substance\n- Maintained warmth",
        "chosen": "Hi [Name],\n\nThank you — that genuinely made my week, especially coming from you. The migration had a few rough patches in the middle that nobody saw, so hearing the end result landed well matters more than I can say.\n\nThanks again,\n[Your Name]"
    },
    # --- global_neutral (5) ---
    {
        "context": "email_refine", "register": "global_neutral",
        "prompt": "Polish this customer apology — it sounds defensive: 'Hi, we received your complaint and looked into it. While I understand your frustration, I should mention that the issue you described was actually due to a third-party provider, not something we did directly. That said, we'll try to do better. Thanks.'",
        "rejected": "Here's a less defensive, more accountable version:\n\n**Subject:** Re: Your Complaint — Apologies and Next Steps\n\n**Body:**\n\nHi [Customer],\n\nThank you for sharing your feedback, and I'm sorry for the experience you had.\n\n**What I want to acknowledge:**\n- The experience was poor regardless of root cause\n- You didn't sign up to manage our vendor relationships\n- We own the end-to-end experience\n\n**What happened:**\n- Third-party provider issue affected your interaction\n- We should have caught and prevented downstream impact\n- We've now flagged this with the provider\n\n**What we're doing:**\n1. Internal review of vendor monitoring\n2. Clearer escalation path for similar issues\n3. Account credit issued to you\n\nAgain, our sincere apologies.\n\nBest regards,\n[Your Name]",
        "chosen": "Subject: Re: your complaint — apologies\n\nHi [Name],\n\nThank you for taking the time to share this. I'm sorry for the experience. It's true that the underlying issue came from a third-party provider, but from your perspective the experience is ours to own — and we didn't catch it in time. That's on us.\n\nI've flagged this with the provider and we're tightening our monitoring so it doesn't happen again. A credit has been applied to your account.\n\nApologies again, and thank you for letting us know.\n\nBest,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "global_neutral",
        "prompt": "Polish this procurement request — it's missing context: 'Hi, please order 10 of the new monitors for our team. Thanks.'",
        "rejected": "Here's a complete version:\n\n**Subject:** Procurement Request — 10 New Monitors for Team\n\n**Body:**\n\nHi [Procurement Contact],\n\nSubmitting a procurement request:\n\n**Item:** Monitor — [Specific model/spec]\n**Quantity:** 10\n**Recipient:** [Team name]\n**Cost center:** [Code]\n**Justification:** Replacing aging monitors; standardization across team\n**Delivery location:** [Office address]\n**Required by:** [Date]\n\n**Approval status:**\n- ✅ Manager: [Name]\n- ✅ Budget: Confirmed under [code]\n\n**Special instructions:**\n- Please consolidate shipping\n- Notify when delivered for distribution\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Procurement request — 10 monitors for the [team] team\n\nHi [Name],\n\nCould you place an order for 10 of the [specific model] monitors for the [team] team? They're replacements for our existing monitors, which are well past their useful life. The cost should go to [cost center], and my manager has already approved it.\n\nDelivery to the [office] location, ideally by [date]. Let me know if you need anything else from my side.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "global_neutral",
        "prompt": "Tighten this status update that meanders: 'Hi everyone, hope you're all having a great week! So I wanted to check in with where we are on the various streams of work, things are mostly going well, the research stream has been moving along nicely with some interesting findings, the build stream is making progress though we had a few small hiccups, and the launch planning stream is on track for now. We'll keep going and update you again next week!'",
        "rejected": "Here's a tighter, more specific version:\n\n**Subject:** Weekly Status Update — All Streams\n\n**Body:**\n\nHi all,\n\nQuick status across the three streams:\n\n**1. Research stream:**\n- Status: 🟢 On track\n- Key finding: [insert]\n- Next milestone: [date]\n\n**2. Build stream:**\n- Status: 🟡 Minor hiccups\n- Issue: [insert]\n- Resolution: In progress\n\n**3. Launch planning:**\n- Status: 🟢 On track\n- Next milestone: [date]\n\n**Next update:** Next week\n\nThanks,\n[Your Name]\n\n**Cuts:**\n- Removed pleasantries\n- Added specificity\n- Clear status indicators",
        "chosen": "Subject: Weekly status — research and launch on track, build slightly noisy\n\nHi all,\n\nWhere we are this week: research is moving along well — we've surfaced [specific finding] which is shaping the build. Build itself is progressing but hit a couple of small snags around [specific area], which we should have cleared by mid-next-week. Launch planning is on track. No risks I'd raise yet.\n\nMore next week.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "global_neutral",
        "prompt": "Polish this stakeholder update — the point is buried at the end: 'Hi all, just wanted to share an update on the integration project. The team has been working hard. We had our weekly sync yesterday and discussed various items. Engineering is making progress on the backend. Marketing is finalizing copy. By the way, the launch is being pushed by two weeks due to a security review finding. Talk soon.'",
        "rejected": "Here's a version with the lead up top:\n\n**Subject:** Integration Project — Launch Pushed by 2 Weeks (Security Review)\n\n**Body:**\n\nHi all,\n\n**Headline:** Launch is moving by 2 weeks due to a security review finding.\n\n**Why:**\n- Security review surfaced an issue\n- Resolution requires additional engineering work\n- Pushing date is safer than rushing fix\n\n**Other updates (for context):**\n- ✅ Engineering: Progressing on backend\n- ✅ Marketing: Finalizing copy\n- ✅ Weekly sync: Held yesterday\n\n**Impact:**\n- Customer comms timing shifts by 2 weeks\n- No change to overall budget\n- Resource plan still holds\n\nWill share revised dates by EOW.\n\nThanks,\n[Your Name]",
        "chosen": "Subject: Integration project — launch pushed by 2 weeks (security review)\n\nHi all,\n\nHeadline first: we're pushing the launch by two weeks because of an issue surfaced in the security review. It's the right call — rushing the fix would create bigger problems downstream.\n\nThe rest of the work continues as planned. Engineering is making good progress on the backend, marketing is finalizing copy, and our weekly sync yesterday didn't surface anything else of concern.\n\nI'll send revised launch dates and customer-comms timing by end of week.\n\nThanks,\n[Your Name]"
    },
    {
        "context": "email_refine", "register": "global_neutral",
        "prompt": "Refine this end-of-quarter thank-you to a partner — too generic: 'Hi, just wanted to send a quick thank you for all your work this quarter. We really appreciate the collaboration and look forward to continuing next quarter. Thanks!'",
        "rejected": "Here's a more specific, sincere version:\n\n**Subject:** Thank You — A Great Quarter Together\n\n**Body:**\n\nHi [Name],\n\nWanted to send a real thank-you note as we close out the quarter.\n\n**What stood out:**\n- Your team's responsiveness on [specific item]\n- The way [person/team] handled [specific challenge]\n- The quality of [deliverable]\n\n**Impact for us:**\n- Hit our [specific outcome]\n- Avoided [risk] thanks to your team's flag\n- Strengthened internal confidence in the partnership\n\n**Looking ahead:**\n- Excited for [upcoming project]\n- Open to feedback on how we can be better partners\n- Same cadence next quarter works well for us\n\nThanks again,\n[Your Name]\n\n**Improvements:**\n- Specific praise over generic\n- Acknowledged impact\n- Forward-looking",
        "chosen": "Subject: Thank you — a strong quarter together\n\nHi [Name],\n\nA real thank-you as we close the quarter. The thing I'll remember most is how your team handled the [specific moment] — that wasn't a small ask, and it's the kind of partnership that makes the difference between vendors and actual collaborators.\n\nLooking forward to next quarter. If there's anything we could be doing better as partners on our end, I'd genuinely value the feedback.\n\nThanks again,\n[Your Name]"
    },

    # ============ CASUAL_REPLY (10) ============
    {
        "context": "casual_reply",
        "prompt": "Reply to a Slack from my manager: 'got a min later today? want to talk through something'",
        "rejected": "Here are some response options:\n\n**If available:**\n- Sure — I'm free after 3, what works?\n\n**If briefly busy:**\n- In meetings till 4 — after that?\n\n**Asking for context:**\n- Yep, of course. Anything I should prep?\n\n**Best practice:**\n- Acknowledge quickly\n- Offer specific window\n- Ask for prep context if useful",
        "chosen": "Yep — I'm free anytime after 3. Anything you want me to prep?"
    },
    {
        "context": "casual_reply",
        "prompt": "Reply to a coworker who Slacked: 'thanks for jumping in on that ticket last night, lifesaver'",
        "rejected": "Here are some response options:\n\n**Brief:**\n- Anytime! Glad it worked out.\n\n**Acknowledging shared effort:**\n- No problem — was a team save honestly.\n\n**Slightly humorous:**\n- Anytime. We'll see whose turn it is next 😅\n\n**Best practice:**\n- Accept gracefully\n- Don't over-deflect\n- Match their energy",
        "chosen": "Anytime — glad we caught it before it turned into something worse. You'd have done the same."
    },
    {
        "context": "casual_reply",
        "prompt": "Reply to a friend via WhatsApp: 'you free this weekend? want to catch up'",
        "rejected": "Here are some response options:\n\n**If yes:**\n- Yeah! Saturday afternoon or Sunday morning works.\n\n**If partly:**\n- Saturday I'm tied up but Sunday is wide open.\n\n**If no:**\n- Ugh, can't this weekend — next one?\n\n**Conversational additions:**\n- Suggest a place\n- Ask what they have in mind\n- Mention how long it's been",
        "chosen": "Yes! Saturday afternoon or Sunday anytime. What were you thinking — coffee somewhere or proper meal?"
    },
    {
        "context": "casual_reply",
        "prompt": "Slack from a coworker: 'what do you think of this new design Figma? https://figma.com/...'",
        "rejected": "Here are some response approaches:\n\n**Quick positive:**\n- Looks great! Love the [specific element].\n\n**Constructive:**\n- Like the overall direction. One thought: [feedback].\n\n**Need more time:**\n- Opening now — give me 15 min and I'll send proper thoughts.\n\n**Best practice:**\n- Be specific\n- Balance positive and constructive\n- Ask questions if context unclear",
        "chosen": "Opening it now — give me 15 minutes and I'll send proper thoughts."
    },
    {
        "context": "casual_reply",
        "prompt": "Slack from PM: 'can you give me an honest read on the timeline? are we actually going to hit it'",
        "rejected": "Here are response options:\n\n**Honest yes:**\n- Honestly, yes — the risky pieces are behind us and the rest is more straightforward.\n\n**Honest no:**\n- Honestly, no. We're going to slip by about a week. Want to talk through why?\n\n**Honest uncertain:**\n- Honestly, 50/50. The [specific risk] is the swing factor.\n\n**Best practice:**\n- Give a real answer\n- Cite the swing factor\n- Offer to discuss",
        "chosen": "Honestly? It's 50/50. The auth migration is the one that could swing it either way — if that goes clean we hit it, if not we slip by about a week. Want to grab 15 minutes to talk through it?"
    },
    {
        "context": "casual_reply",
        "prompt": "WhatsApp from my sibling: 'amma's bday is next week, what should we get her?'",
        "rejected": "Here are some response approaches:\n\n**Offer ideas:**\n- What about [item 1] or [item 2]?\n\n**Throw it back:**\n- I'm stuck too — any thoughts so far?\n\n**Suggest collaboration:**\n- Let's split something nice — that lehenga she liked?\n\n**Practical questions to ask:**\n- Budget?\n- Practical or sentimental?\n- Surprise or together?",
        "chosen": "Honestly I'm blank — any thoughts so far? Maybe we just go together on something nicer instead of separate gifts?"
    },
    {
        "context": "casual_reply",
        "prompt": "Slack from a new intern: 'is it okay if I ask you a really basic question?'",
        "rejected": "Here are some response options:\n\n**Reassuring:**\n- Always — basic questions are the best kind. Shoot.\n\n**Brief and warm:**\n- Of course, ask away.\n\n**With invitation:**\n- Yes please — no such thing as too basic. What's up?\n\n**Tone tips:**\n- Make them feel safe\n- Keep it warm\n- Invite, don't just permit",
        "chosen": "Always. No such thing as too basic — shoot."
    },
    {
        "context": "casual_reply",
        "prompt": "Slack from someone director-level: 'loved your demo today, very impressive'",
        "rejected": "Here are some response options:\n\n**Gracious:**\n- Thank you, that really means a lot coming from you!\n\n**Sharing credit:**\n- Thanks! Couldn't have pulled it off without [names].\n\n**With acknowledgment of next steps:**\n- Thank you — there's still work to do but glad it landed well.\n\n**Best practice:**\n- Don't deflect entirely\n- Acknowledge gracefully\n- Share credit if relevant",
        "chosen": "Thank you — that really does mean a lot coming from you. The team did the heavy lifting; happy to share more on what's next whenever works."
    },
    {
        "context": "casual_reply",
        "prompt": "Slack from a teammate: 'any chance you can cover my 2pm sync? something came up'",
        "rejected": "Here are some response options:\n\n**Yes:**\n- Yes, I got it — anything I should know going in?\n\n**Yes with constraint:**\n- I can cover, just send me the agenda quickly.\n\n**No with apology:**\n- Ugh sorry, I'm in another sync at 2. Try [colleague]?\n\n**Best practice:**\n- Respond fast\n- Ask for prep info\n- Suggest alternative if can't",
        "chosen": "Yep, got it — drop the agenda and any context I need in this thread before then."
    },
    {
        "context": "casual_reply",
        "prompt": "Slack from a coworker I haven't seen in a while: 'we miss you at lunch, where've you been?'",
        "rejected": "Here are some response options:\n\n**Brief:**\n- Aw, miss you all too! Been swamped — will rejoin soon.\n\n**Honest:**\n- Honestly burning out a bit, eating at my desk. Tomorrow?\n\n**Light deflect:**\n- Hiding from my inbox. Coming back tomorrow.\n\n**Best practice:**\n- Be warm\n- Suggest re-joining\n- Match their casual tone",
        "chosen": "Aw, miss you all too — just been in heads-down mode for a couple weeks. Coming back tomorrow, save me a seat."
    },

    # ============ SHORT_EXPLAIN (8) ============
    {
        "context": "short_explain",
        "prompt": "A dev asked why our team uses rebase instead of merge for feature branches. Quick explanation?",
        "rejected": "Here's the rationale:\n\n**Why rebase:**\n- **Linear history:** Easier to read and bisect\n- **No 'merge commit' noise:** Cleaner log\n- **Forces engagement with conflicts:** No silent merges\n\n**Why not merge:**\n- Merge commits create branching history\n- Harder to trace what happened when\n- Bisecting bugs becomes painful\n\n**Trade-offs:**\n- Rebase rewrites history (be careful on shared branches)\n- Slightly steeper learning curve",
        "chosen": "Mostly because rebase keeps the git history linear, which makes it much easier to read later and way easier to bisect when something breaks. Merge commits work fine, but they leave a tangled history that nobody wants to dig through six months later. The catch is that rebase rewrites commits, so you have to be careful not to rebase shared branches."
    },
    {
        "context": "short_explain",
        "prompt": "A new joiner asked why we run a retro every sprint. How do I explain in a couple of lines?",
        "rejected": "Here's the reasoning:\n\n**Why every sprint:**\n- **Catch issues early:** Before they become entrenched\n- **Team voice:** Everyone gets to flag what's not working\n- **Continuous improvement:** Small adjustments compound\n- **Psychological safety:** Regular forum for honest input\n\n**Common objections:**\n- 'Too frequent' — but skipping means losing the rhythm\n- 'Same issues come up' — that's signal, not noise\n\n**Format:**\n- 30-45 minutes\n- What went well / what didn't / what to try next",
        "chosen": "Because problems that don't get aired immediately tend to become permanent. A short retro every sprint gives everyone a regular, low-stakes forum to flag what's not working before it calcifies. The same issues coming up multiple sprints in a row is actually useful signal — it tells us we haven't really fixed them yet."
    },
    {
        "context": "short_explain",
        "prompt": "Someone asked why we don't allow direct database access in production. Quick explanation?",
        "rejected": "Here's the reasoning:\n\n**Why we block direct access:**\n- **Safety:** Easy to accidentally drop a table\n- **Audit trail:** Hard to trace who did what\n- **Performance:** Ad hoc queries can take down prod\n- **Security:** Credentials sprawl\n\n**Approved alternatives:**\n- Read-only analytics replicas\n- Service-level APIs\n- Break-glass access with logging\n\n**Trade-offs:**\n- Slower for debugging\n- More upfront tooling",
        "chosen": "Mostly because direct prod access is one accidental command away from disaster — and even when nothing breaks, there's no good audit trail of who touched what. We route everything through a read-only analytics replica or service APIs, and there's a break-glass option with full logging when something is on fire. Slightly slower for debugging, but worth it."
    },
    {
        "context": "short_explain",
        "prompt": "A coworker asked why we A/B test almost every change. How do I explain?",
        "rejected": "Here's the rationale:\n\n**Why we A/B test:**\n- **Avoid intuition errors:** Designs that 'feel right' often lose\n- **Quantify impact:** Real metrics, not vibes\n- **De-risk rollouts:** Catch regressions in small populations\n- **Learn fast:** Even null results teach us\n\n**Limits:**\n- Not everything is testable\n- Sample size matters\n- Sometimes 'just ship it' is right for small changes",
        "chosen": "Mostly because product intuition is unreliable — even great PMs and designers ship things they're sure will win, and those things lose in tests more often than people expect. A/B testing also de-risks rollouts; we'd rather find out a change tanks engagement when it's exposed to 1% of users than 100%. Not everything needs a test, but anything that touches a key metric usually does."
    },
    {
        "context": "short_explain",
        "prompt": "Someone asked why we have a no-meeting Wednesday. Quick explanation?",
        "rejected": "Here's the reasoning:\n\n**Why no-meeting Wednesday:**\n- **Focus time:** Continuous block for deep work\n- **Cognitive load:** Meetings fragment attention\n- **Maker schedule vs. manager schedule:** Engineers need long stretches\n- **Productivity:** Most ICs report Wednesdays as most productive\n\n**What it doesn't block:**\n- True emergencies\n- Customer-facing meetings\n- 1:1s if both parties opt in",
        "chosen": "Because deep work needs uninterrupted stretches, and a single meeting in the middle of an afternoon can effectively kill the whole afternoon. Giving everyone one fully clear day a week means engineers actually get a real shot at the hard problems. True emergencies and customer meetings can still happen — it's just the default that's flipped."
    },
    {
        "context": "short_explain",
        "prompt": "A new dev asked why we use TypeScript instead of just plain JavaScript. Explain in a couple lines.",
        "rejected": "Here's the breakdown:\n\n**Why TypeScript:**\n- **Catches bugs at compile time:** Not in production\n- **Self-documenting:** Types are documentation\n- **IDE support:** Autocomplete, refactoring\n- **Confidence:** Easier to refactor large codebases\n\n**Trade-offs:**\n- Build step required\n- Slight learning curve\n- More code upfront for simple scripts",
        "chosen": "Mostly because types catch a whole class of bugs before the code ever runs — the kind that you'd otherwise discover at 2am when a user reports them. They also make IDE tooling much smarter, so refactoring stops being terrifying. The upfront cost is a bit more typing and a build step, but it pays for itself many times over once the codebase is non-trivial."
    },
    {
        "context": "short_explain",
        "prompt": "A junior dev asked why we have on-call rotations instead of just a dedicated ops team. How do I explain?",
        "rejected": "Here's the rationale:\n\n**Why we rotate:**\n- **You build it, you run it:** Devs feel the pain of bad design\n- **Better systems:** Knowledge of failure modes informs architecture\n- **Shared load:** No one team burns out\n- **Empathy with users:** First-hand experience of outages\n\n**Trade-offs:**\n- Stressful for ICs\n- Sleep disruption\n- Needs good runbooks and tooling",
        "chosen": "Because if developers never get paged for their own code, they tend to build systems that are painful to operate. Rotating on-call closes that feedback loop — the next architecture decision you make is much smarter after you've been woken up at 3am by your own service. The trade-off is real stress, so it depends on good runbooks and reasonable rotation schedules."
    },
    {
        "context": "short_explain",
        "prompt": "Someone asked why we have a 24-hour cooldown rule before merging code reviews. Quick explanation?",
        "rejected": "Here's the reasoning:\n\n**Why 24 hours:**\n- **Async review quality:** Reviewers in different time zones\n- **Avoid rubber-stamping:** Discourages 'LGTM' under pressure\n- **Thinking time:** Tough changes deserve a second read\n- **Quality bar:** Forces a real, considered look\n\n**Exceptions:**\n- Hotfixes\n- Trivial changes (with override flag)\n- Pre-approved spikes",
        "chosen": "Mostly to give reviewers — especially in other time zones — a fair shot at actually reading the change. Without the cooldown, PRs tend to get rubber-stamped to unblock the author, and that's where bugs sneak in. There's an override for hotfixes and a trivial-changes flag, so it doesn't get in the way when it shouldn't."
    },

    # ============ DIVERSITY BALLAST (2) ============
    {
        "context": "narrative",
        "prompt": "Describe a really good cup of coffee you've had.",
        "rejected": "A memorable coffee experience — details:\n\n**Setting:** Small specialty café\n**Time of year:** Cool autumn morning\n**Coffee:** Pour-over, single origin Ethiopian\n\n**Tasting notes:**\n- Bright acidity\n- Floral notes\n- Hints of berry\n- Long, clean finish\n\n**Why it stood out:**\n- Perfect brew temperature\n- Quiet, focused atmosphere\n- First sip on an empty stomach\n- Brewed by someone who cared",
        "chosen": "There's a small place I went to one autumn morning in a city I was only visiting for two days. I asked for whatever they were excited about, and the guy behind the counter lit up and started talking about an Ethiopian he'd just opened. He brewed it as a pour-over without breaking eye contact. It came out almost orange in the cup. The first sip tasted like jasmine and tart berries and somehow nothing like the coffee I usually drink. I sat there for an hour. I have tried to find that coffee again. I never have."
    },
    {
        "context": "explanatory",
        "prompt": "Briefly explain why songs get stuck in your head.",
        "rejected": "Why songs get stuck in your head — explained:\n\n**The phenomenon:** Earworm (involuntary musical imagery)\n\n**Mechanisms:**\n- **Brain pattern completion:** Memory loops on incomplete patterns\n- **Catchy structure:** Repetitive, simple melodies stick best\n- **Recency and exposure:** Recent listens dominate\n- **Emotional tagging:** Songs tied to memories are stickier\n\n**Research:**\n- Most common songs: Pop hits with predictable hooks\n- Average duration: Minutes to hours\n- Triggers: Stress, fatigue, idle mind\n\n**How to break the loop:**\n- Listen to the full song\n- Chew gum\n- Engage in absorbing tasks",
        "chosen": "It's a quirk of how your brain handles unfinished patterns — when you hear a fragment of a song, your memory keeps trying to complete it, and the simpler and catchier the hook, the more your brain obliges. Researchers actually call this an 'earworm,' and the songs most likely to do it tend to share traits: repetitive, easy melodies that loop neatly. The classic trick to dislodge one, weirdly enough, is to listen to the song all the way through — your brain marks the pattern as resolved and lets it go."
    },
]


def main() -> None:
    path = Path("data/formatting_pairs_v1.jsonl")
    assert path.exists()
    existing = set()
    with path.open() as f:
        for line in f:
            existing.add(json.loads(line)["prompt"])
    new = [r for r in ROWS if r["prompt"] not in existing]
    with path.open("a") as f:
        for row in new:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    counts = Counter()
    reg = Counter()
    with path.open() as f:
        all_rows = [json.loads(line) for line in f]
    for r in all_rows:
        counts[r["context"]] += 1
        if "register" in r:
            reg[r["register"]] += 1
    print(f"Appended: {len(new)} new (skipped {len(ROWS)-len(new)} dupes)")
    print(f"Total: {len(all_rows)}\n")
    for c, n in sorted(counts.items()):
        print(f"  {c:18} {n}")
    print()
    for r, n in sorted(reg.items()):
        print(f"  {r:20} {n}")


if __name__ == "__main__":
    main()
