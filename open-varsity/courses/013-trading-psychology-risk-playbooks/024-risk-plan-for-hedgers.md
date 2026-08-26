Chapters
Module D · Complete Risk Plans by User Type - Chapter 24
# Risk Plan for Hedgers
What exposure is actually being hedged, the hedge size, its cost, its expiry, and when to remove it - a clean process so a hedge protects you instead of quietly becoming a second bet.
Plan
What you'll learn
  * ·Define the exposure
  * ·Hedge size
  * ·Hedge cost and expiry
  * ·When to remove a hedge
  * ·Hedge vs new position
  * ·A one-page hedger plan


Arjun ran a stock portfolio of about Rs 50,00,000. The week before the Union Budget he got nervous - budgets can move markets hard - so he shorted some NIFTY futures to protect himself. Sensible. The budget came and went quietly, nothing dramatic happened, and Arjun got busy with work. He simply forgot the short was still there. Over the next two months NIFTY drifted up about 8%. His stocks gained nicely on paper, but his forgotten short futures lost almost exactly the same amount. In a clearly rising market he had made nothing - and paid margin and carrying costs for the privilege. His insurance had quietly turned into a bet against his own portfolio.
That is the one mistake this chapter is built to prevent. A hedge is a temporary tool with a job and an end date. The moment you forget about it, it stops being protection and becomes a second position you never meant to hold.
## A hedge is a borrowed umbrella, not a new home
Think of a hedge like an umbrella you borrow because rain is forecast. You open it for the storm, and when the sky clears you close it and give it back. You do not keep walking around indoors holding it open. A hedge works the same way: you put it on for a specific risk, hold it while that risk is active, and take it off when the risk has passed. Leave it open too long and it just gets in your way - and costs you.
Key idea
A hedge is a disciplined, temporary tool, not a position you forget. Define exactly what you are protecting, size it, price it, give it an expiry, and decide when it comes off - before you ever place it.
Everything below is one process, in five steps. Walk through all five before any hedge, and the hedge stays a hedge.
## Step 1 - Define the exposure (name it, or you cannot hedge it)
This is the step beginners skip, and skipping it ruins everything after. Before you hedge, write down three things in one plain sentence:
  * **Which position** you are protecting (a specific stock, a basket, a futures position, a future cash need).
  * **How much** of it - the rupee value at risk.
  * **Against what** - the exact risk. A market-wide crash? A single result? A currency move?


"I feel nervous about the market" is not an exposure. It cannot be sized or priced or ended, so it cannot be hedged - it can only be worried about. "My Rs 50,00,000 equity portfolio, against a sharp fall over the next two weeks around the budget" - _that_ you can hedge, because every word turns into a number later.
## Step 2 - Size the hedge (full or partial, using beta and notional)
Now decide how much protection to buy. Two ideas from the hedging module do the work: **notional value** (the full rupee value your hedge controls) and **beta** (how much your holding tends to move when the index moves - a beta of 1.2 means it moves about 20% more than NIFTY).
A worked example. Arjun's book is Rs 50,00,000 with a beta of roughly 1.2 to NIFTY.
  * Beta-adjusted value to hedge = 50,00,000 x 1.2 = **Rs 60,00,000**.
  * Say NIFTY is near 24,000 and the lot is about 65 (lot sizes are revised periodically by the exchange - always check the current contract specs), so one futures lot controls 24,000 x 65 = **Rs 15,60,000** of notional.
  * Full hedge = 60,00,000 / 15,60,000 = **about 3.8 lots**. He cannot trade a fraction of a lot, so a full hedge means about 4 lots and a partial hedge means fewer.


A **full hedge** aims to cancel the whole move. A **partial hedge** - say 2 lots, roughly Rs 31,20,000 of notional - softens a fall while leaving room to still gain if the market rises. Most beginners over-hedge: they buy more protection than their exposure, which silently turns the hedge into a fresh directional bet the moment the market moves their way. Match the hedge to the exposure, never bigger.
## Step 3 - Know the all-in cost before you place it
A hedge is insurance, and insurance has a premium. Add up the whole bill _before_ you commit, not after:
  * For a **protective put** : the option premium (e.g. a put at Rs 200 x 65 = Rs 13,000 per lot), plus brokerage, STT, and the bid-ask spread you cross.
  * For a **futures hedge** : the margin blocked, the carrying cost, and - the big one - the **upside you give up** if the market rises while you are short.


If protecting Rs 50,00,000 for two weeks costs you Rs 45,000 all-in, that is roughly 0.9% of the book. Is that worth it for this risk? Sometimes yes, sometimes the honest answer is "just trim the position instead." You can only judge once you know the number.
## Step 4 - Match the expiry to the risk window
A hedge has a life span; make it cover the danger and not much more. If your risk is a budget on a known date, pick an option or futures expiry that comfortably _includes_ that date - not one that expires the day before, leaving you naked at the worst moment. If the exposure runs for a quarter, you may have to roll a monthly hedge forward. Match the hedge's life to the risk window: too short and it lapses before the danger passes; too long and you pay for protection you no longer need.
## Step 5 - Decide when to remove it (before you enter)
Write the exit rule at the same time you write the entry. The trigger is simple: **the hedge comes off when the exposure is gone.**
  * Hedging an _event_? Remove it the session after the event is digested.
  * Hedging a _position_? Remove the hedge when you sell or trim that position.
  * Reaching _expiry_? Make an explicit choice - roll or remove - never let it auto-forget.


Set a calendar reminder the day you put the hedge on. Arjun's whole loss came from missing this one step.
The life of a hedge: put it on, hold, remove risk window Put it on just before the risk Hold through while the risk is active Remove it risk has passed forget to remove = accidental bet A hedge has a beginning and an end. Skip the end and it becomes a position you never chose.
Common mistake
Two mistakes turn a hedge into a wound. The first is **a hedge with no exit** : you put it on, the risk passes, and you forget it - so a short hedge bleeds in a rising market (Arjun) or a long put quietly decays to nothing. Always set the removal trigger and a reminder before you enter. The second is **hedging an undefined risk** : "I'm scared" cannot be sized, priced, or ended, so the hedge wanders with no off-switch. If you cannot name the exposure in one sentence, you are not hedging - you are guessing, and paying for it.
## Your one-page hedger plan
Fill this in - on paper or in a note - before you place any hedge. If any line is blank, you are not ready.
  * **Exposure:** I can name the position, its rupee value, and the exact risk in one sentence.
  * **Size:** I have sized the hedge from beta and notional, and chosen full or partial on purpose (never bigger than the exposure).
  * **Cost:** I know the all-in cost - premium or margin, spread, charges, and upside given up - and it is worth it for this risk.
  * **Expiry:** The hedge's life covers the whole risk window, with a plan to roll if the risk outlasts it.
  * **Exit:** I have written the removal trigger ("comes off when ___") and set a calendar reminder for it.
  * **Sanity check:** This is a hedge, not a view. If I just want to bet on a fall, I should say so and size it as a bet, not hide it inside "protection."

The one-page hedger plan Fill every row before you place the hedge 1 Exposure Which position, how much, against what risk - in one sentence 2 Size Full or partial - from beta x notional, never bigger than the exposure 3 Cost All-in bill - premium or margin, spread, charges, upside given up 4 Expiry Cover the whole risk window - roll if the risk outlasts the hedge 5 Exit Written removal trigger + a reminder - comes off when the risk is gone Five rows. A blank row means the hedge is not ready.
## How hedging differs by who you are
The five steps are the same for everyone, but what fills them in changes a lot. The removal trigger especially: it is always "when the exposure ends" - but the exposure means something different for each person.  
| User type  | What they hedge  | Typical tool  | Risk window  | When to remove  |  
| --- | --- | --- | --- | --- |  
| Long-term investor  | A concentrated stock or whole portfolio, against a crash or a known event  | Protective put or short index future  | The event, or until the holding is trimmed  | After the event, or when the position is sold  |  
| F&O trader  | Overnight gap risk on an open leveraged position  | An opposite leg, a further-OTM option, or smaller size  | Often hours to one expiry  | When the position is closed or the event passes  |  
| Business  | A real cash flow - an importer's dollars, an input-cost commodity  | Currency or commodity futures or forwards  | Matched to the invoice or payment date  | When the underlying cash flow actually settles  |  
The business case is the cleanest teacher: the hedge exists _only_ because a real payment is coming, and it ends the day that payment is made. Every good hedge should feel that tied to something real.
## When this fails
This process makes hedges disciplined. It does not make them magic. Be honest about the limits.
**Basis risk.** An index hedge does not perfectly track _your_ stocks. The index can hold while your specific shares fall, leaving you hedged on paper and still losing. The hedge reduces risk; it rarely cancels it.
**Chunky instruments.** Lot sizes mean you often cannot hedge a small book precisely - one NIFTY lot may be larger than your whole portfolio. You are left choosing between over-hedging and not hedging, and over-hedging is the trap that creates an accidental bet.
**Cost drag from over-hedging your nerves.** If you hedge every wobble, the premiums and given-up upside bleed you slowly. Not every risk is worth insuring. As the earlier chapters said: a small book, a long SIP, or a tiny position is usually better left alone than hedged.
**A hedge cannot fix a position that is simply too big.** If the only way you sleep is by hedging, the real answer may be a smaller position. Cutting is often cheaper and cleaner than protecting.
This is education, not personalised advice. The point is the discipline - name the exposure, size it, price it, time it, and end it - so your protection stays protection and never becomes a bet you forgot you placed.
## Quick self-check
**1.** Why is "I feel nervous about the market" not something you can hedge?
Because it has no size, no price, and no end. A hedge needs a named exposure - which position, how much, against what risk - so it can be sized, costed, given an expiry, and removed. A vague feeling has no off-switch.
**2.** How did Arjun's hedge turn into a losing bet?
He shorted NIFTY futures before the budget but never removed the short after the event passed. As the market rose about 8% over two months, the forgotten short lost roughly what his stocks gained - so his insurance became an accidental bet against his own portfolio, plus margin and carrying costs.
**3.** How do beta and notional help you size a hedge?
Beta tells you how much your holding moves versus the index, so you scale the amount to hedge by it (a Rs 50,00,000 book at beta 1.2 needs about Rs 60,00,000 hedged). Notional is the rupee value one futures lot controls, so dividing the two gives the number of lots for a full hedge.
**4.** What should the expiry of a hedge match?
The risk window. Choose an expiry that comfortably covers the danger - not one that lapses the day before the event - and plan to roll the hedge if the exposure outlasts a single expiry.
**5.** When should a hedge be removed?
When the exposure is gone: the session after an event is digested, the moment you sell the position you were protecting, or by an explicit roll-or-remove decision at expiry. Write the trigger and set a reminder the day you put the hedge on.
On this page
