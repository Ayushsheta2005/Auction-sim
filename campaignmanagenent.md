3.6
designing and running campaigns
Targeting and LTV models, the basic building blocks of a targeting
system, provide a solid foundation for efficient marketing decisions.
A marketing campaign, however, is typically a flow with multiple ac-
tions and decisions geared to achieve a certain objective. This flow may
require multiple models to be wired together and optimizations to be
done with multiple signals and constraints taken into account. A target-
ing system often has some sort of repository for campaign templates,
where each template describes a certain flow of actions and decisions.
This flow is typically designed for a certain objective, but it can be
parametrized with different targeting models, budgeting constraints,
user experience properties, and so on. Forecasting of the campaign3.6 designing and running campaigns
ROI and optimization of the execution parameters and thresholds to
balance the costs and profits is an important part of the campaign de-
sign process, and the corresponding routines and models can be con-
sidered as part of the template. In this section, we consider several
types of campaigns and their relationship to the previously discussed
basic models.
3.6.1
Customer Journeys
From an economic standpoint, interactions between a customer and
brand can often be viewed as a collection of transactions that can
be characterized in terms of total amounts, purchased items, margins,
clicks on the website, and so on. The problem of marketing optimiza-
tion can also be viewed in a transaction-centric way so that all compo-
nents of the marketing mix become focused on the optimization of in-
dividual transactions, in terms of their probabilities and margins. The
notion of the customer life cycle puts this optimization into a broader
context but still focuses on the brand’s concerns and objectives rather
than the customer experience. This approach is incomplete in many
marketing environments, including retail, where interactions with a
customer are experience-centric and the success of a brand is deter-
mined by its ability to deliver a superior long-term customer experi-
ence, rather than optimizing individual transactions.
One popular approach to customer experience analysis and model-
ing is based on the notion of customer journey maps. A journey map
tells the story of the relationship between a customer and the brand.
The map can describe the entire arc of the engagement, similarly to
the life-cycle curve, or can be focused on a specific scope, such a single
purchase. The map is typically visualized as a diagram with the steps
or stages of the engagement and the transitions between them. A very
simplified example of a customer journey map is shown in Figure 3.17.
This map depicts the flow of a single transaction but puts it in the con-
text of the customer experience and long-term interactions with the
brand.
The journey starts with triggers, which include browsing for a new
idea and product, preparation for special events such as birthday par-
ties, getting a promotional email, or the necessity to replenish a con-
sumable product. The trigger is followed by researching product in-
formation and selecting the purchasing channel. The interaction then
continues in the scope of the selected channel, including browsing of
a specific product and checkout, and completes with post-purchase ac-
tions such as product return or writing a customer review. In real life,
customer journey maps are typically much more complicated and in-
121122
promotions and advertisements
Figure 3.17: Example of a customer journey map.
clude a lot of details about the customer behavior and decision-making
process, distribution of customers by different states and branches, and
so on. In addition, customer journey maps are often created for each
customer segment because the journeys can differ substantially across
the segments.
A marketing campaign typically has a certain footprint on the jour-
ney map, in the sense that a campaign attempts to influence the path of
a customer. In Figure 3.17, for example, customers who drop out of the
offline purchasing funnel are provided with an offer to win them back.
Each campaign can be viewed as a type of template that can be applied
to a specific situation in the customer journey. A programmatic system
can have a repository of campaign templates, where each template in-
cludes the rules that prescribe when the campaign actions should be
triggered and how the situation should be handled, along with mod-
els to estimate the parameters of the required actions and forecast the
outcomes. A template can describe a single action or a whole set of ac-
tions that can be executed at different points in time, by using different
channels, and by taking the observed feedback into account.3.6 designing and running campaigns
Analysis of customer journeys and the creation of journey maps is
usually a strategic project that often includes extensive analytical re-
search, customer surveys, and marketing strategy development. Thus,
the creation of customer journeys maps and campaign templates is not
the responsibility of a programmatic system. We generally assume that
these artifacts are created elsewhere and then entered into the system.
The responsibilities of the system, however, include estimation and op-
timization of the template parameters and dynamic selection of the
most optimal templates.
3.6.2
Product Promotion Campaigns
One of the most basic types of targeted campaign is a sales promotion
for an individual product. Examples of such promotions include ad-
vertisements without monetary value, dollar-off coupons, buy-one–get-
one (BOGO) coupons, and free product samples. In the CPG domain,
this class of campaign is often referred to as free-standing inserts (FSI),
named so because of coupon booklets that are inserted into local news-
papers. In the most basic form, a standalone promotion corresponds
to a simple customer journey with a trigger (promotion) and purchase
(redemption). As we will see later, this approach is not necessarily the
most efficient one, but it is applicable to all objectives:
• For acquisition, a brand can send BOGO or dollar-off coupons
to customers who are heavy category buyers but do not buy this
particular brand.
• For maximization, a brand can send conditional promotions like
Buy 3, Get $1 Off to existing customers.
• For retention, a brand can send BOGO or dollar-off promotions
to customers who have decreased their consumption relative to
previous purchasing cycles.
The response modeling framework provides some guidance on how
such promotions can be targeted by using predictive models that esti-
mate the probability of response, but there are many additional aspects
that need to be covered, including the targeting process, budgeting
rules, and selection of promotion parameters.
3.6.2.1
Targeting Process
A targeting system can be used in both batch and real-time modes,
depending on the environment and campaign nature. Some promo-
tions can be distributed by sending millions of emails in one shot, so
123124
promotions and advertisements
a targeting system can prepare a list of customers to be targeted in
advance. Other promotions are targeted in near real time because of
rapidly changing customer profiles or context. For example, a promo-
tion may or may not be offered to customers depending on the content
of their shopping baskets just before checkout. The real-time approach
is generally more flexible, and a properly designed real-time targeting
system can also simulate the batch mode by evaluating the targeting
rules and models for the entire customer database. Consequently, we
focus on the real-time targeting case and consider a process that re-
ceives a single customer profile and the corresponding context as the
input and produces a list of promotions that should be offered to this
customer.
We also assume that the system has a database of available promo-
tions that can potentially be offered. This database includes promotions
from all campaigns that are currently active. Each promotion needs
to be attributed with properties such as business objective, promoted
product, and category, so the targeting system can use this informa-
tion to link the promotion with the proper targeting models and rules.
This is the reason why promotion creation and targeting are closely
related to each other, in the sense that each targeting step or feature
requires a counterpart in the campaign configuration and promotion
attributes. We will go though the targeting process and discuss both
how promotions are selected from the set of available options and the
methodology for creating and attributing promotions with the proper-
ties and conditions needed for targeting.
The targeting process can be thought of as a sequence of three steps.
First, the system takes all available promotions and selects those that
are valid for a given context and customer. Next, promotions are scored
to produce a list sorted according to the fit to the objective. Finally,
the optimal set to be offered to the customer is selected by applying
budgeting limits and other constraints. This process is sketched in Fig-
ure 3.18. The initial filtering of promotions is typically based on busi-
ness rules and conditions, so we refer to it as hard targeting. On the
other hand, promotion scoring typically uses predictive models that
produce a continuous score, so we call this stage soft targeting.
The goal of the hard-targeting stage is to select promotions that qual-
ify for a given context. Promotions created in the targeting system are
typically associated with conditions that must be met by a given con-
text to activate the promotion. The purpose of these conditions is to
encourage certain consumer behaviors and ensure the basic economic
goals of the promotion. The hard-targeting conditions essentially de-
fine the campaign template, that is, the point in the customer journey3.6 designing and running campaigns
Figure 3.18: The promotion targeting process.
where the promotion should be applied. Consider the following typical
examples:
• Quantity condition. Activates a promotion when the customer
purchases a certain quantity of a certain product, brand, or cate-
gory in a single transition or over a certain period of time. This
condition is often used in maximization campaigns to stretch a
consumer, that is, to give an incentive to buy more then usual.
For example, a customer who typically buys two packs of yogurt
can be offered a Buy 4, Get 1 Free promotion.
• Non-buyer condition. Activates a promotion for customers who
have not bought a product or brand for a certain period of
time. This condition can be used in retention and acquisition
campaigns to separate active brand customers from inactive and
prospecting consumers.
• Channel condition. Activates a promotion when a customer inter-
acts with a brand or retailer via a certain channel. For example, a
customer can be rewarded for visiting a store three times a week.
• Retargeting condition. Activates a promotion based on previ-
ously offered or redeemed promotions. For example, customers
who have received but have not redeemed promotions via digital
channels can be contacted by using in-store channels.
• Location condition. Activates a promotion based on the customer
location as determined from mobile device data, store location,
in-store beacons, or IP address.
125126
promotions and advertisements
• Availability condition. Some promotions can be temporarily de-
activated if the corresponding products are out of stock or un-
available through a given marketing channel.
The hard-targeting step produces a set of promotions that can poten-
tially be offered to a consumer. The goal of the soft-targeting stage is
to select the most relevant offers and filter out options that are likely to
be inefficient. Soft targeting is often done by using propensity models.
A targeting system can maintain a repository of models where each
model is trained for a certain business objective and product category
and is attributed accordingly. As each promotion is also attributed with
similar properties, the system can dynamically link models to promo-
tions. Scoring models can be combined with special conditions that
complement the logic encapsulated in the model. For instance, the ba-
sic look-alike acquisition model identifies customers who are similar
to natural triers, but it does not ensure that a promotion will not be of-
fered to those who already buy the product. In contrast, maximization
and retention promotions typically should not be offered to customers
who do not consume the promoted product. These additional checks
can be implemented as a condition.
3.6.2.2
Budgeting and Capping
Once the set of candidate promotions is prepared and ranked, the sys-
tem needs to select the final set of promotions that can be offered to
the customer. This step can include several controls to manage differ-
ent aspects of a campaign. First, the number of promotions received
by a customer in the scope of a single campaign, as well as the total
frequency of communications with the customer (number of messages
per time unit), should be limited. These rules, often referred to as pres-
sure rules or frequency capping rules, typically use thresholds selected
heuristically or by means of experimentation. Next, the campaign bud-
get or the total number of issued promotions is typically limited. The
targeting system, however, often needs to determine the optimal num-
ber of promotions to maximize the campaign ROI. It can be the case
that this number is far below the limit specified by the marketer and
consumption of the budget up to the limit can make losses. From the
propensity modeling standpoint, the profitability optimization prob-
lem can be viewed as finding the propensity scoring threshold that
maximizes the profit if all customers with a higher score are targeted
and all other customers are not. We have already shown how the trade-
off between campaign costs and profits can be modeled by using the
response modeling framework, and we now consider an example that
provides more practical details.3.6 designing and running campaigns
example 3.4
Consider the case of a retailer who has 100,000 loyalty card holders.
The retailer plans a targeted campaign where each promotion instance
costs $1 and the potential profit of one response is $40. The average re-
sponse rate for this type of campaign and product category estimated
from historical data is 2%. On the basis that we have created a propen-
sity model that estimates the response probability for each customer,
we can score all card holders and sort them by the scores. The result
can be summarized by splitting the customers into “buckets” of equal
size where the first bucket corresponds to the customers with the high-
est scores and the last bucket corresponds to those with the lowest
scores. The targeting problem can then be defined as finding the opti-
mal number of top buckets to include in the targeting list, or, equiva-
lently, finding the threshold score that separates these top bucket from
the bottom ones. We use bucketing for the sake of convenience in this
example and this approach is often used in practice as well, but there is
nothing to stop us from doing the same calculations for individual cus-
tomers, that is, having as many buckets as customers. Let us assume
that we have 10 buckets or deciles, so that each bucket contains 10,000
customers; consequently, the average expected number of responders is
200 per bucket. In other words, we are likely to get 200 responses from
each bucket if we randomly assign customers to buckets. This number
is shown in the second column of table 3.7, and the third column con-
tains the cumulative number of responders, which reaches 2,000 or 2%
of the customer base in the bottom row.
Decile
1
2
3
4
5
6
7
8
9
10
Responses, Random
Bucket
TotalPr
200
200
200
200
200
200
200
200
200
2000.060
0.057
0.038
0.017
0.010
0.007
0.006
0.003
0.001
0.001
200
400
600
800
1,000
1,200
1,400
1,600
1,800
2,000
Responses, Targeted
Bucket
Total
600
570
380
170
100
70
60
30
10
10
600
1,170
1,550
1,720
1,820
1,890
1,950
1,980
1,990
2,000
Lift
3.00
2.93
2.58
2.15
1.82
1.58
1.39
1.24
1.11
1.00
Table 3.7: Example of campaign lift calculations.
Next, let us assume that the lowest response probability scores gener-
ated by the propensity model in each bucket are those presented in the
fourth column. By multiplying the bucket size by this probability, we
127
128
promotions and advertisements
get the expected number of responses in the case of the targeted distri-
bution presented in the next two columns. The total number of respon-
ders still adds up to 2,000, of course. The ratio between the number of
responders in the case of targeted and random distributions is called
lift, and it is the key metric that describes the quality of the targeting
model. The lift is typically visualized by using a lift chart similar to the
one in Figure 3.19. This chart shows two lines that correspond to the
cumulative number of responses: the straight line corresponds to the
random distribution and the raised curve to the targeted distribution.
Figure 3.19: Lift chart for the targeting model.
To determine the number of buckets to be targeted, we need to esti-
mate the campaign ROI. Each promotion costs $1, so the random dis-
tribution strategy is not profitable because each bucket causes a loss:
$40 response profit  10,000 recipients  0.02 response rate
$1 per customer  10,000 recipients
  $2,000
The targeted campaign, however, will be profitable for the first three
buckets because of the high response rates, as summarized in table 3.8.
One can see that including more buckets initially increases the cam-
paign ROI but it then starts to decrease and eventually becomes nega-
tive.
The campaign ROI is maximized for outreach to three buckets, that
is, the top 30% of the population. This corresponds to all customers
with a propensity score above 0.038. The targeted campaign ROI is
plotted in Figure 3.20. Note that the maximum possible budget, which3.6 designing and running campaigns
Decile
1
2
3
4
5
6
7
8
9
10
RandomProfit
TargetedTargeted
ROI
-2,000
-2,000
-2,000
-2,000
-2,000
-2,000
-2,000
-2,000
-2,000
-2,00014,000
12,800
5,200
-3,200
-6,000
-7,200
-7,600
-8,800
-9,600
-9,60014,000
26,800
32,000
28,800
22,800
15,600
8,000
-800
-10,400
-20,000
Cost
10,000
10,000
10,000
10,000
10,000
10,000
10,000
10,000
10,000
10,000
129
Table 3.8: Example of campaign profitability calculations.
corresponds to sending a promotion to each and every customer, does
not maximize the ROI. On the contrary, it causes a loss of $20,000.
Figure 3.20: Targeted campaign ROI as a function of the outreach.
It is important to note that we used the basic response probability,
instead of uplift modeling, in this example. In practice, this can result
in poor campaign performance because high response rates do not
guarantee uplift in customer spending or consumption. In other words,
a control group in each bucket can perform equally well or even better
than the targeted group in the same bucket. One can work around this
problem by replacing the response probabilities in table 3.7 with the
uplift scores discussed in Section 3.5.4.2.
N130
promotions and advertisements
The ROI maximization principle allows estimation of the optimal
baseline parameters of a campaign, such as the total number of promo-
tions to be distributed and the scoring threshold. In the real world, it
can sometimes be beneficial to deviate from the baseline, especially for
real-time applications when the set of customers who will actually in-
teract with the system is not known in advance. Consider the following
scenario. A system runs a promotional campaign with a fixed budget
and spreads this budget evenly over the campaign’s time frame. This
suggests that we should use some fixed distribution rate, for example,
100 promotions per hour. However, what should we do if the campaign
is running over this target rate (in our example, 100 promotions have
already been issued during the last hour) but we encounter a consumer
with a very high propensity score? It can be reasonable to go over the
budget at this point and then slightly decrease the rate later to get back
on track. This behavior can be implemented by dynamic adjustment of
the scoring thresholds depending on the deviation from the target dis-
tribution rate. This idea is illustrated in Figure 3.21. We define the tar-
get distribution rate and and two margins, ε and ε , that determine
the maximum acceptable deviation from the target line. Note that the
target does not necessarily have to be a straight line, and one can use
a more sophisticated curve that takes into account weekends, working
hours, and so on. The actual distribution rate is constantly measured
and controlled by the system to stay within the margins.
Figure 3.21: Dynamic scoring threshold for budget control.
The scoring threshold can then be expressed as a function of the de-
viation from the target line at the current moment of time t0 . If we are
substantially under budget (under the ε line), the scoring threshold
can be set to the minimum, which corresponds to the lowest affinity
L0 between the consumer and promotion that is sufficient to make the3.6 designing and running campaigns
offer. If we are substantially over budget (above the ε line), then the
threshold should be set to the maximum possible scoring value to stop
the distribution completely. These two extreme points can be connected
by some growing function, as illustrated in Figure 3.21. Consequently,
we become more and more demanding of consumers as we approach
and cross our budgeting limits, and we lower the bar when we do not
encounter enough high-quality prospects.
3.6.3
Multistage Promotion Campaigns
Standalone promotion campaigns, such as the distribution of trial or
maximization coupons, are widely used in practice. However, it can
be argued that this strategy can be inefficient because it has a very
short and limited impact on the customer journey [Catalina Marketing,
2014]. It is sometimes possible to design more sophisticated campaigns
with multiple phases that influence the customer journey over a longer
period of time. Let us consider an example of a CPG maximization
campaign with the following design:
• The first phase of the campaign is an announcement that aims to
inform the customers about the offer. For example, a brand can
distribute the following message via available marketing chan-
nels: Buy Q or more units of product X and save on your next shopping
trip. The more you buy, the more money you save.
• The second phase is distribution. A targeting system tracks the
transactions and issues dollar-off coupons to customers who
qualify for the targeting condition, that is, the purchase of Q or
more units in this example. The discount amount of the coupon
is determined dynamically based on the purchased quantity –
as announced, the more consumers buy, the more they save. At
this stage, a consumer is incentivized to buy more units to get a
coupon as a reward.
• The third and the last phase is redemption. On the second shop-
ping trip, the consumer buys the promoted product to redeem
the coupon issued in the previous stage. The consumer is incen-
tivized to buy a product to redeem a coupon and get a discount.
This campaign template can be thought of as a customer journey
with three steps: trigger, purchase, and redemption. It can be argued
that this approach is more efficient than standalone promotions be-
cause it has a more durable impact on customer loyalty and lower
costs per unit moved [Catalina Marketing, 2014]. The dynamically de-
termined discount value in the second stage is an interesting detail
131132
promotions and advertisements
because the targeting system needs to optimize this value and fore-
cast how it will influence the campaign outcomes. This aspect is not
addressed by the targeting and budgeting processes discussed in the
previous sections. Let us consider an example that demonstrates how a
targeting system can heuristically evaluate different promotion param-
eters and forecast the campaign outcomes by using just basic statistics.
More formal discount optimization methods will be discussed later in
Chapter 6 in the context of price optimization.

example 3.5
Consider the case of a promotional campaign that follows the three-
phase scenario described above. The goal of the targeting system is
to choose a reasonable value for the quantity threshold Q and, in the
second phase, to determine the discount amount based on the quantity
that is actually purchased. We can start with a histogram of purchase
quantities for the promoted product calculated for the time interval
equal to the duration of the campaign. Let us denote the number of
transactions with exactly q units of the promoted product purchased
as Hpqq, so the historical histogram is as follows:
Hp1q  4000 (32%)Hp4q  1000 (8%)
Hp3q  2000 (16%)Hp6q  0
Hp2q  5000 (40%)
Hp5q  600 (5%)
We want to stretch customers who buy relatively small quantities,
so the system can select threshold Q to be above the majority of trans-
actions. In this example, the value of 3 would be a reasonable choice
because 72% of transactions are under this threshold. Consequently,
the system will offer a discount coupon to customers who buy more
than 3 units. The discount value depends on the quantity actually pur-
chased. We will discuss this in more detail in Chapter 6, but we can
assume for now that the discount values are static configuration pa-
rameters. For example, suppose that the minimal discount value is 15%
and it increases by 5% at each level. This means that customers who
buy 3 units get the discount of 15%, those who buy 4 units get 20%,
and those who buy 5 units get 25%. Let us denote the number of units
at level i as qi and the corresponding discount value as di . Once all
of these parameters are determined, the system can forecast the cam-
paign outcomes. This can be done separately for each discount level.
The expected number of coupons generated at level i can be estimated,
based on the previously created histogram, as
couponspiq  Hpqi q
(3.32)3.6 designing and running campaigns
133
The expected number of redemptions can then be estimated by using
a response model that includes the discount depth as a feature:
redemptionspiq  couponspiq  rpdi q
(3.33)
in which rpdi q is the average response rate predicted by the model. The
cost of coupons at level i can then be estimated as
costpiq  pproduct price  di  qi
cq  redemptionspiq
(3.34)
in which c stands for the additional costs associated with a coupon,
such as distribution and clearing-house costs. The campaign efficiency
can be predicted as the ratio between the total number of redemptions
and the total costs summed over all levels (cost per redemption).
3.6.4
Retention Campaigns
Retention campaigns aim to save customers who are likely to leave.
This type of campaign is widely used in telecommunications, insur-
ance, banking, and other subscription-based domains where the conti-
nuity of a relationship is critical. The problem of customer churn, how-
ever, is relevant for most non-subscription businesses as well, including
retail. One of the key reasons why retention activities are important is
that acquisition of new customers can be much more challenging and
expensive than the retention of existing ones. According to some stud-
ies, the acquisition cost per consumer can be 10–20 times higher than
the retention or reactivation cost because of lower response rates and
other factors [Artun and Levin, 2015].
A retention campaign can be defined as a follow-up with customers
who are at risk. The follow-up and risk, however, can be defined very
differently depending on the campaign design. Examples of risk in-
clude the risk of subscription cancellation and the risk of switching
to a different supermarket chain. The definition of risk depends on the
business model, nature of the product or service, and usage patterns. A
software service provider, for example, can be concerned about the risk
of subscription cancellation but may also observe a significant number
of customers who create an account but do not download the client
application. Thus, the risk of not downloading the application can be
recognized and addressed by a dedicated retention campaign. Exam-
ples of follow-up actions include reminder emails, distribution of edu-
cational materials, requests to review the recently purchased product,
and special offers and discounts.
Compared to promotional campaigns, the design of retention cam-
paigns puts more emphasis on the lifetime value and uplift. The in-
N134
promotions and advertisements
corporation of lifetime value projections is important because invest-
ments in the retention of customers with low value would be mean-
ingless. Uplift modeling is important because targeting of the wrong
customers can be counterproductive for several reasons [Radcliffe and
Simpson, 2007]. First, many customers at risk are dissatisfied already,
and additional communications, especially intrusive ones like phone
calls, can catalyze the churn process. Second, some retention commu-
nications can remind customers that they have an opportunity to leave,
which makes them reconsider their relationship with the brand and
look around for alternative options. This makes it important for the
communications to be focused and the outcomes to be constantly mea-
sured by using control groups.
Retention campaigns are typically assembled by using the standard
building blocks, but there exist different design methods. One of the
most basic approaches is to target based on the propensity to churn.
This model can be created by using standard propensity modeling
methods with a training data set assembled from active and churned
customer profiles. This approach is seemingly simple, but it has pit-
falls that should be discussed. As we have previously discussed, a
marketing action can be described in terms of two conditional prob-
abilities – the probability to respond if treated and the probability to
respond without treatment. In the case of retention, the response event
corresponds to churn. All customers can be categorized with respect
to these two probabilities, as depicted in Figure 3.22.
Figure 3.22: Categorization of customers from the perspective of a retention
campaign.
If the overall retention strategy is focused, that is, the customers are
not normally treated with retention offers, a propensity model trained3.6 designing and running campaigns
to predict churn outcomes will actually predict the probability of churn
given no treatment as
scorepxq  Prpchurn | N, xq
(3.35)
in which x is the customer profile feature vector. A retention campaign
driven by this probability focuses on the rightmost vertical slice of
the square in Figure 3.22, which includes many Persuadables but also
many Lost Causes. If the retention strategy is broad, that is, almost all
customers are treated to some degree, the model will actually estimate
the propensity to churn under treatment as
scorepxq  Prpchurn | T , xq
(3.36)
which corresponds to the horizontal area at the top of the square in
Figure 3.22, which contains many Do-not-disturbs and Lost Causes.
This aspect of modeling should be taken into account when the popu-
lation for model training is selected. The retention campaign can also
use survival analysis to estimate the time-to-churn, which can be more
convenient for choosing the right moment for treatment than the prob-
ability of churn.
Targeting customers based on their probability to churn does not
take into account the long-term outcomes of the campaign. These out-
comes can be quantified in terms of lifetime value because every reten-
tion saves the LTV of the corresponding customer and every churn is a
loss of this LTV. If the probability to churn and LTV are estimated for
a given customer, the product of these two values is the expected loss.
We can expect that the ratio between the saved revenues and the cam-
paign costs is maximized by treating those customers with the highest
expected loss, so this measure can be used as a targeting score:
scorepxq  Prpchurn | N, xq  LTVpxq
(3.37)
The LTV can be estimated based on the average customer spend or
by using the more advanced LTV models described earlier. This model
can be customized depending on the business model to account for
the costs and profits associated with the different possible outcomes.
For example, the expected retention gains, churn losses, and campaign
costs can be separately estimated. The expected loss model specified by
equation 3.37 is widely used in practice because of its simplicity and
reasonably good efficiency.
135136
promotions and advertisements
The main shortcoming of the expected loss model is that it uses only
the probability to churn and not the churn uplift, that is, the difference
between the treated and non-treated churn probabilities:
upliftpxq  Prpchurn | T , xq  Prpchurn | N, xq
(3.38)
A positive churn uplift means that the treatment amplifies the churn,
that is, the treatment has a negative effect. High uplift corresponds to
the upper left corner of the square in Figure 3.22. A negative churn up-
lift means that the treatment decreases the churn, which corresponds
to the lower right corner in Figure 3.22. Consequently, we want to tar-
get customers by using the inverse of the uplift as a score:
scorepxq  upliftpxq  savabilitypxq
(3.39)
This metric is also called savability because it estimates the propen-
sity to react positively to the retention activity. Uplift/savability can
be modeled by using the methods described in Section 3.5.4.2, includ-
ing the two-model and single-model approaches. Similarly to other
applications of uplift modeling, the savability-based approach helps to
separate those customers who are likely to stay only if they are treated
from other groups, thereby increasing the efficiency of the retention
campaign. However, it is important to keep in mind that this approach
also inherits the typical disadvantages of uplift modeling. It includes
more complicated modeling and higher variance of estimates because
the uplift is the difference of two random variables. The uplift can also
be combined with the expected loss technique to take into account the
long-term impact on the harvested LTVs:
scorepxq  savabilitypxq  LTVpxq
(3.40)
Once the targeted scores are calculated, the optimal targeting depth,
that is, the percentage of the population to be targeted, can be deter-
mined by using the ROI maximization method described earlier in Sec-
tion 3.6.2.2. The campaign can then be executed with the same target-
ing process as that used for product promotional campaigns.
3.6.5 Replenishment Campaigns
Retention campaigns are most relevant for subscription-based busi-
nesses, such as telecommunication services, insurance, software, and
banking. In the retail domain, the subscription-based model is less
frequently used, but many products are routinely replenished so the
engagement model becomes similar to a subscription. Examples of re-
plenishable products are numerous: food, cosmetics, office supplies,3.7 resource allocation
accessories like water filters, and many others. Replenishment cam-
paigns aim to drive repeat purchases and decrease purchasing cycles by
sending reminders, recommendations, and specialized promotions.
From the campaign design standpoint, the distinctive features of re-
plenishment are the emphasis on communication timing and purchas-
ing habits. The communication timing is important because the replen-
ishment notifications should be aligned with the individual purchasing
cycles – it is not efficient, for example, to send a notification immedi-
ately after a customer has purchased the product. Connection with the
purchasing habits is also important because the notification message
should be consistent with the products and categories typically pur-
chased by the recipient.
Let us start with a very basic approach that can be implemented by
a targeting system. First, the system estimates the average duration of
a purchasing cycle for each replenishable product or product category.
The replenishment campaign is then executed repeatedly, for exam-
ple, on a daily basis. For each execution, the system goes through the
customer profiles and determines the last purchasing date for replen-
ishable products. This date is compared with the estimated duration
of the purchasing cycle, and a notification is sent to customers who
are apparently approaching the end of the cycle. The message can be
personalized based on the most recently or most frequently purchased
products found in the purchasing history.
One of the main limitations of the above approach is an estimate of
replenishment cycles that is too rough. One possible improvement is
to break down the estimate not only by product category but also by
customer segment or persona, to account for the differences between
customers. In other words, the cycle duration is estimated for each pair
of a category and a persona. More accurate results can be obtained by
using survival analysis to estimate the time-to-purchase, as we have
already discussed. The survival model also allows the determination
of the factors that positively or negatively contribute to the time-to-
purchase, such as discounts or replenishment notifications themselves,
so the message content and frequency can be adjusted accordingly.
3.7
resource allocation
The problem of optimal targeting can be viewed as a resource allo-
cation problem where some limited resource, such as sales coupons,
needs to be allocated across customers. So far, we have focused only on
this type of allocation and have ignored the fact that marketing activi-
ties may be required to make many other allocation decisions. The cor-
porate marketing resource allocation strategy generally includes alloca-
137138
promotions and advertisements
tion between marketing and non-marketing activities, products, prod-
uct life-cycle stages, markets and territories, business objectives, mar-
keting channels, and communication types [Carpenter and Shankar,
2013]. Many of these allocation decisions, such as allocation between
marketing and research activities, are very strategic and thus cannot be
addressed by a programmatic system. Some other decisions are more
tactical, and the system can include modules that automate or at least
facilitate the decision-making process. It should be kept in mind, how-
ever, that targeting is one of the most tactical and technical allocation
problems, and the automation of other allocation decisions is increas-
ingly more complex and challenging.
The modeling and optimization of how resources are allocated
across marketing activities and capabilities is known as marketing mix
modeling (MMM). It can be viewed as the statistical analysis of how
the different components of the marketing mix, such as promotions
and prices, impact business performance metrics, such as sales and
revenues. In this section, we focus on two resource allocation problems,
allocation by channel and allocation by business objective, and discuss
how these problems can be addressed by using MMM methods.
3.7.1
Allocation by Channel
A targeting system often has multiple marketing channels at its dis-
posal, and each channel has its own costs structure, audience, and
efficiency. The direct mail channel, for example, may have a much
higher cost per message than the email channel, but it may provide
higher response rates for certain categories of customers. This requires
marketing communications to be optimized with respect to channels.
One possible approach to this problem is optimization at a customer
level, where the channel is selected by using a response model that
accounts for channel-specific response probabilities and costs. Another
approach is to optimize the global budget allocation across channels
to maximize the revenue. This is sometimes referred to as channel mix
modeling. These two methodologies can be viewed as bottom-up and
top-down solutions, respectively, and both are important.
Channel mix modeling is a set of statistical analysis methods that
focuses on the following descriptive and predictive questions:
• What percentage of revenue (or other performance metric) is
driven by each channel or communication type?
• How will an increase or decrease in a given channel spend affect
the revenue?
• What is the optimal budget allocation across the channels?3.7 resource allocation
Intuitively, we can expect these questions to be answered by a re-
gression model that expresses the metric of interest as a function of the
channel activity. The challenge is that the dependency between the ac-
tivity and the observed metric can be complicated for several reasons.
First, we can directly measure the channel activity only as the current
number of emails or online advertising impressions, but the customer
responses are typically delayed and spread over time. Second, multi-
ple campaigns can overlap when they run in parallel, but we can only
observe the cumulative effect. Finally, the dependency between the in-
tensity of the channel activity and the magnitude of the response is
often nonlinear because of saturation effects. One popular channel mix
model that accounts for these effects is the adstock model [Broadbent,
1979].
The key assumption made by the adstock model is that each given
sales period retains a fraction of the previous stock of advertising. By
assuming, for now, that we have only one advertising channel, let us
denote the intensity of the channel activity measured in dollars spent
or the number of messages in time period t as xt , the business metric
of interest, often the sales volume or revenue, as yt , and the current
effect induced by the activity on the business metric as at . The effect
variable at is called the adstock. The adstock model assumption can
then be expressed as
at  xt
λ  at1
(3.41)
in which λ is the decay parameter that corresponds to the fraction of
the effect carried over the time period. For example, a parameter of
0.4 means that the treatment from one period ago has 40 percent of
its effect during the current period. In other words, the adstock model
assumes that each new marketing activity increases loyalty and aware-
ness to the new level, but loyalty gradually fades until it is boosted
again by the next portion of activity. By expanding recursive equa-
tion 3.41, we get
at  xt
λxt1
λ2 xt2
λ3 xt3
...
(3.42)
Note that this is essentially a smoothing filter applied to the input
sequence. In practice, we can always assume that the treatment effect
is finite and limited by n periods, so we rewrite the adstock transfor-
mation of the original sequence as
at  xt
ņ

j 1
λj  xtj
(3.43)
The observed business metric is then estimated as a linear function
of the adstock:
pt  wat
y
c
(3.44)
139140
promotions and advertisements
in which w is the weight and c is the baseline value given no adstock.
In the case of multiple channels, we assume that the adstock is additive,
so the full model specification is a linear regression over the adstocks:
ņ
pt 
y

wi ait
c
(3.45)
i 1
whereby each channel is modeled with its own decay parameter λi ,
so the full model requires estimation of the baseline parameter c, n
decay parameters λi , and n channel weights wi . We can fit the model
by solving the following problem for the observed samples yt :
min
c, w, λ
¸
 yt

 ypt 2
(3.46)
t
The fitted model allows us to estimate the impact of increasing or de-
creasing the channel budgets and to measure the relative contribution
of each channel to the target metric as:
w a
zit  ° i it
j wj ajt
(3.47)
This value can be averaged over time to obtain the average relative
channel contribution. The efficiency of the channel can be measured as
the ratio between the absolute channel contribution and the channel
budget, that is, the number of units sold generated by each dollar spent
on marketing activities through this channel. The following example
illustrates how the adstock model can be created and used.

example 3.6
Consider a retailer who uses two marketing channels: email and SMS.
The retailer can measure and control the intensity of marketing com-
munications through each of the channels by setting budgeting and
capping rules. The retailer also observes the sales volume. A data sam-
ple with these metrics is plotted in Figure 3.23 for 20 sequential time
intervals (we have omitted the table with numerical values for the sake
of space).
The adstock model can be fitted by solving problem 3.46 with numer-
ical optimization methods. By setting the length of the decay window
n to 3, we get the following estimates for the model parameters:
baseline:
email:
SMS:
c  28.028
λemail  0.790
λsms  0.482
wemail  1.863
wsms  4.8843.7 resource allocation
141
Figure 3.23: Data for adstock modeling: sales volume, email activity, and SMS
activity.
We can use these parameters to calculate the adstock for each of
the channels according to expression 3.43. The structure of the sales
volume can then be visualized as three layers stacked one on top of the
other: the baseline sales volume determined by constant c, the email
contribution estimated as the email adstock scaled by wemail , and the
SMS contribution estimated as the SMS adstock weighted by wsms . This
structure corresponds to expression 3.45, and the result is plotted in
Figure 3.24. This decomposition enables us to estimate the efficiency of
each channel and optimize budget allocation.
The basic adstock model accounts for overlapping marketing activ-
ities and decay effects but not for the advertising saturation that we
mentioned earlier. In general, an increase in the treatment intensity
increases the outreach of the campaign, which increases the demand.
The dependency between the intensity and demand, however, is not lin-
ear. It typically follows the law of diminishing returns, so that spending
more dollars on the marketing activity at some point yields a lower in-
cremental demand. The adstock model can account for this saturation
effect by nonlinear transformation of the intensity variable. One pos-
N142
promotions and advertisements
Figure 3.24: Decomposition of the sales volume into the layers contributed by
different marketing channels.
sible choice is to use the sigmoid (logistic) function, so that recursive
adstock equation 3.41 is redefined as follows:
at 
1
1
exppµ  xt q
λ  at1
(3.48)
in which µ is an additional model parameter that controls the steepness
of the logistic curve. The adstock model can be extended or modified
in many ways to account for additional effects that can be found in
practice. For example, we typically need to account for the seasonality
of demand, which can be done by extending the model with additional
variables. At this point, channel mix modeling can take advantage of
the demand modeling techniques discussed in detail in Chapter 6. An-
other example is that the geometric lag assumption made by the ad-
stock model is somewhat restrictive because the time lag can have a
more complex shape. In fact, the model described by equations 3.42
and 3.43 is known in econometrics as the Koyck distributed lag model,
which, in turn, belongs to the family of distributed lag models [Koyck,
1954]. This family provides a number of more flexible alternatives, in-
cluding a polynomial distributed lag model, which can be both more
flexible and easier to estimate than the Koyck model [Almon, 1965;
Hall, 1967].
3.7.2
Allocation by Objective
A programmatic system can use both LTV growth and acquire–
maximize–retain goals as the input objectives for the targeting3.7 resource allocation
optimization. The ROI can be estimated in all of these cases by using
the LTV uplift or immediate net profit uplift, in accordance with the
response modeling framework. The choice between these objectives
and global optimization of the ROI is a strategic question that does
not necessarily need to be addressed by a programmatic system.
However, the system can provide some guidance on how to allocate
budgets across the objectives to maximize the overall ROI [Blattberg
and Deighton, 1996].
We have discussed in Section 3.5.7 that the retention rate is a major
factor that influences the LTV, so the LTV can be considered a function
of the retention rate. We can make the assumption that the retention
rate is, in turn, a function of the marketing budget spent on retention
activities. For example, we can model the dependency between the
budget and rate as follows:

r  rmax 1  ekr R
(3.49)
in which R is the retention budget per customer, rmax is an estimate
of the maximum retention rate (ceiling) that we can achieve given the
unlimited budget, and kr is a coefficient that determines how fast the
rate approaches the ceiling. Similarly, we can model the acquisition
rate a (response rate for an acquisition campaign) as a function of the
acquisition budget:

a  amax 1  eka A
(3.50)
in which A is the acquisition budget per customer, amax is an estimate
of the maximum response rate, and ka is a parameter that controls the
sensitivity of the rate to budget changes. Consequently, the acquisition
net profit for a given customer can be defined as
a  LTVprq  c
(3.51)
in which c is the acquisition cost per prospect. The overall optimization
problem for budgets A and R can then be defined as follows:
max
A, R
subject to
Np pa  LTVprq  cq
A
R ¤ total budget
Nc  LTVprq
(3.52)
in which Np is the total number of available prospects and Nc is the
total number of current customers. The first term of equation 3.52 cor-
responds to the revenues from new customers and the second term cor-
responds to the revenues from existing customers, so it is effectively a
revenue optimization problem. Equation 3.52 defines the optimization
problem in terms of aggregated and averaged values, but it can be eas-
ily rewritten as a sum of individual LTVs over all customers to enable
more accurate estimations with predictive models.
143144
promotions and advertisements
3.8
online advertisements
The principles of promotion targeting discussed in the previous sec-
tions are geared towards consumer packaged goods and the traditional
retail environment. It is clear that many of these principles hold for
other marketing environments, but implementation heavily depends
on the available data and exact definition of business objectives, which
can vary across environments. We continue here by analyzing online
advertising, which is perhaps the most important and well-developed
application of algorithmic marketing and is an excellent example of
an environment where the technical infrastructure and data flows are
so complicated that the business objectives cannot be understood and
achieved without careful examination of the technical capabilities and
limitations.
3.8.1
Environment
The online advertising environment is very complex and diverse be-
cause it represents a marketplace where thousands of companies sell
and buy ad inventory, offer and utilize technical systems that automate
the buying process, and control and measure the quality and effective-
ness of advertising campaigns. Additional complexity comes from the
fact that, although most of the terminology and standard offers are
generally accepted across the industry, there are many variations and
cross-cutting solutions that appear as the industry evolves. The high
complexity of the online advertising ecosystem makes it difficult to
capture all important aspects of the environment in a single view, so
we will start with a simplified model, shown in Figure 3.25, to support
our discussion of business objectives and economic goals.
Figure 3.25 depicts the relationships between the following key enti-
ties that constitute the online advertising landscape:
• A brand, also commonly referred to as a marketer, is a seller of
products or services. The brand invests money into advertising
campaigns and expects to obtain a return on the investments by
improving certain aspects of sales and customer relationships.
• An advertiser or agency runs advertising campaigns on behalf
of the brand. The advertiser generally tries to achieve the same
goals as the brand, but its exact strategy depends on the pay-
ment model established between the brand and the advertiser, as
well as the methodology used to measure the performance of the
campaign. The brand can work with multiple agencies that may
compete against each other in the scope of one campaign.3.8 online advertisements
Figure 3.25: Online advertising environment.
• The advertisers can reach an internet user, who is a current or
potential client of the brand, through different channels. Examples
of channels include ad banners on a web page, paid results on
a search-engine result page, and online video ads, among others.
In a general case, the set of channels is not limited to internet
channels and can include other media, like TV ads or printed
catalogs.
• Each channel is represented by multiple publishers, for example,
websites. Publishers sell their ad inventory, that is, the available
slots that can contain the actual ads.
• The publishers and advertisers are connected by means of an
ad exchange. The exchange receives ad requests from publishers
when a piece of inventory becomes available (e. g., an internet
user opens a web page) and distributes the requests across ad-
vertisers, who, in turn, can buy the available ad slot and show
the ad to the user. The exchange is often organized as a Vick-
rey (second-price) auction that processes each ad request in real
time, so the exchange is commonly referred to as a real-time bid-
ding (RTB) process.
145146
promotions and advertisements
• A user is the recipient of the ads delivered via the channels. The
user can interact with multiple channels and publishers over
time, receiving ad realizations known as impressions. From the
brand perspective, the user either eventually converts to produce
some desired outcome, such a purchase on the brand’s website,
or does not convert. Consequently, there is a funnel of sequential
impression events Ai for each user that ends with the outcome
Y, as shown in Figure 3.25.
• Finally, the impressions and conversions are tracked by an attri-
bution system. We consider the attribution system as an abstract
entity that can trace the user identity across channels and pub-
lishers and can keep records of which user received which im-
pression from which advertiser at which point in time. The pur-
pose of the attribution system is to measure the effectiveness of
the ad campaign and provide insights into the contributions of
individual channels, advertisers, and user segments. The attribu-
tion system typically collects the information by using tracking
pixels attached to ad banners and conversion web pages; users
are identified with web browser cookies. However, the attribu-
tion process can consume additional data sources, such as pur-
chases in brick-and-mortar stores, correlate this data with online
profiles by using loyalty or credit card IDs, and measure causal
effects across online and offline channels.
In the environment model above, the brand relies on the attribution
system to measure the effectiveness of individual advertisers and ad
campaigns as a whole. The metrics produced by the attribution sys-
tem directly translate into the advertiser’s fees and the brand’s costs
and revenues, so we will spend the next section examining attribution
models and their impact on advertiser’s strategies.
3.8.2
Objectives and Attribution
Similarly to the case with promotions, the business objectives of the
brand are driven by a desire to shift the relationships with certain con-
sumers from one level to another:
brand awareness The marketer is generally interested in making
its brand recognizable to potential customers and making it as-
sociated with a certain category of products, such as soft drinks
or luxury cars, even if this does not immediately translate into
conversions.
customer acquisition Acquisition aims to attract prospects who
do not interact with the brand and drive them to conversion.3.8 online advertisements
retargeting Retargeting, also known as remarketing, focuses on
prospects who have already interacted with the brand, where
there is potential to develop the relationship with them. A typi-
cal example is internet users who visited the brand’s website one
or more times but did not convert.
These primary objectives can be complemented by additional con-
straints that are important for the brand. For example, the brand
might not be willing to advertise on websites with adult, violent,
or hateful content. Ideally, the contract between the brand and the
advertiser should be designed in such a way that the advertiser is
paid for achieving the objectives above. More specifically, the desired
properties of the contract can be described as follows:
• The targeting and bidding processes should be driven by the
business objective of the campaign (e. g. , brand awareness, acqui-
sition, or retargeting) and be restricted by additional rules such
as brand safety.
• The effect of the campaign should be measurable, and the metrics
should accurately reflect the value added by the advertiser. In
other words, the metrics should answer the question “What will
happen with the business objective if the advertiser is removed?”
Note that this question directly relates to the uplift modeling
discussed earlier in this chapter.
• It should be possible to answer the above question about adver-
tiser removal for the case of multiple advertisers working for the
same brand. Credits should be attributed to advertisers propor-
tionally to their contribution to the total value increment.
Unfortunately, it is not straightforward to define a contract that fully
meets the above criteria. The business objectives can be formalized in
different ways, and the measurement of the incremental value also rep-
resents a non-trivial statistical and technical problem. Let us first de-
scribe several basic methods that are widely used in practice, and we
will then discuss the outstanding questions and limitations that should
be addressed in later sections.
From the brand perspective, the overall effectiveness of the campaign
can be measured by using the cost per acquisition (CPA), which is de-
fined as the total cost of the campaign Ccamp divided by the total num-
ber of conversions Nconv :
CPA 
Ccamp
Nconv
(3.53)
Conversion, however, can be defined in different ways. One possible
approach is to count post-view actions, that is, to count the users who
147148
promotions and advertisements
visited the brand’s site or made a purchase within a certain time in-
terval (for example, within a week) after they received an impression.
A more simple method is to count the immediate clicks on advertise-
ments, which is referred to as the cost per click (CPC) model. From the
advertiser perspective, it makes sense to split the cost of the campaign
into a product of the number of impressions and the average cost of
one impression, so the CPA metric can be expressed as follows:

CPA 
Nimpr  E cimpr
Nconv


1
 E cimpr
 CR

(3.54)
in which Nimpr is the total number of impressions delivered by the


campaign, E cimpr is the average price paid by the brand for one
impression, and CR is the conversion rate. The advertiser’s margin is
the difference between the price paid by the brand and the bid value
placed in the RTB, so we can define the advertiser’s equivalent of the
CPA as follows:
CPAa 


1

E cimpr  cbid
CR
(3.55)
We need to specify contracts for cimpr and cbid in order to evaluate
the above expressions for CPA and CPAa . The price cimpr paid by the
brand is typically fixed, although there are two different types of con-
tracts that are used in practice:
• Cost per action , also known as cost per acquisition (CPA) or pay per
acquisition (PPA), contract. The brand pays a fixed fee for each
conversion measured by the attribution system.
• Cost per mile (CPM) contract. The brand pays a fixed fee for each
impression, but eventually measures the overall CPA by using
the attribution system.
Both approaches are equivalent in the sense that the advertiser has
to minimize the CPA metric to satisfy the client, even for CPM con-
tacts. The fixed fee implies that the CPA metric in equation 3.54 can
be optimized by maximization of the conversion rate CR. However, the
bid value cbid in equation 3.55 is not fixed and directly influences the
conversion rate, so optimization of the CPAa metric requires joint op-
timization of CR and cbid .
The final area we need to cover is attribution in the case of multi-
ple advertisers. The most basic approach is last-touch attribution (LT),
which gives all the credit to the last impression that preceded the con-
version. Consequently, the goal of the advertiser under the LT model is
to identify customers who are likely to convert immediately after the
impression.3.8 online advertisements
The CPA and LT assumptions – we will refer to these settings as the
CPA-LT model – provide a reasonably complete and formal problem
definition that can be used for targeting process optimization. However,
the CPA-LT model is overly simplistic and has a number of issues and
limitations:
• There is no explicit relationship with the business objective. The
model does not distinguish acquisition, awareness, or retargeting
goals. In fact, CPA-LT principles are geared towards consumers
with a high propensity to purchase, which implies a heavy bias
towards retargeting and tactical acquisition rather than aware-
ness and strategic acquisition.
• The model suggests optimization of the response, not uplift. This
can lead to meaningless results under certain circumstances. For
example, a targeting method that identifies only high-propensity
users who are likely to convert without any impressions will have
a very good performance under the CPA-LT model, although this
is unlikely to be a good approach from the ROI standpoint.
• Last-touch attribution encourages advertisers to cheat and pig-
gyback on each other’s efforts. For example, an advertiser can
buy a lot of low-quality inventory, such as ad slots at the bot-
tom of web pages, to “touch” as many use users as possible (the
so-called carpet bombing).
We will discuss how to optimize targeting and bidding strategies
under the CPA-LT model in the next section, and we will then investi-
gate how the shortcomings of this model can be addressed with more
sophisticated attribution and controlled experiments.
3.8.3
Targeting for the CPA-LT Model
The basic goal of targeting under the CPA-LT model is to identify users
who are likely to convert shortly after the impression. Similarly to the
case of promotion targeting, we use a variant of look-alike modeling to
solve this problem, but we want to explicitly account for the informa-
tion about a user’s response to advertisements as opposed to selecting
natural buyers based on purchase histories. In particular, we want to
account for the performance of the currently running advertisement,
which means that we have to dynamically adjust our targeting method
based on the observed results. In other words, we want to build a self-
tuning targeting method.
We can assume that the advertiser has the following data for each
consumer profile:
149150
promotions and advertisements
• Visited URLs. The advertiser listens to bid requests and other
partner data sources that allow the user’s browsing history
to be captured. URLs can include both the domain, such as
google.com, and the address of a particular page.
• User attributes. The advertiser can receive additional information
about the user along with the URLs: for example, the proper-
ties of a browsing device and applications, geographical location,
time spent on a page, and some others.
• Bids and impressions. The advertiser can track the bids it made
for a given user and the impressions delivered to the user.
• Ad clicks. The advertiser can get information on how the user
interacted with the delivered ads.
• Conversions. The brand can provide the advertiser with informa-
tion about the conversions on its website.
• Additional brand data. The brand can provide additional data,
such as products browsed by a user on the brand’s website.
The features for predictive modeling can be engineered based on these
data elements. Visited URLs and derived characteristics, such as re-
cency and frequency, are known to carry a lot of predictive informa-
tion about conversions. A major challenge, however, is a high number
of observed URLs, in that a model that consumes a binary vector where
each element, zero or one, indicates whether a user visited a URL or
not, might have millions of dimensions.
The straightforward approach for the problem of self-tuning target-
ing is to start the campaign with random targeting, that is, to bid for
random people, wait for a sufficient number of conversions, and then
train the scoring model by using converted users as positive examples
and non-converted users as negative examples, as shown in Figure 3.26.
This approach, however, is not optimal because conversion events are
very rare in the case of random targeting and the dimensionality of
user profiles, as discussed above, is very high, so the creation of a suf-
ficient training data set by using random bidding at the beginning of a
campaign can be impractically expensive [Dalessandro et al., 2012a].
There are many different techniques that can help to improve the
basic approach described above. In the rest of this section, we closely
follow the staged targeting methodology described in the work of [Da-
lessandro et al., 2012a] and [Perlich et al., 2013], which provides a com-
prehensive practical solution for self-tuning targeting. The approach
is to perform the targeting process in three sequential steps: calculate3.8 online advertisements
Figure 3.26: Desirable sampling for the targeting task. The shaded circles corre-
spond to positive and negative examples.
the brand proximity, incorporate the ad response, and incorporate the
inventory quality and calculate the bid amount.
3.8.3.1
Brand Proximity
The goal of this step is to estimate the probability of conversion Y re-
gardless of the ad impact, that is, to calculate the unconditional brand
proximity PrpY | uq for user u. If historical information about visitors to
the brand site is available before the campaign begins, the advertiser
can create models for a converting user by selecting converted profiles
as positive examples and random profiles of internet users as negative
examples. Note that this sampling is different from the desired sam-
pling depicted in Figure 3.26. This step is essentially look-alike mod-
eling that uses visited URLs as features and conversions as labels to
model the unconditional brand proximity:
ϕpuq  PrpY | uq
 PrpY | URL1 , . . . , URLn q
(3.56)
in which URLi are binary labels equal to one if the user visited the
corresponding URL and zero otherwise. The advertiser can use differ-
ent definitions of the URL and conversion to build multiple models
ϕu1 , . . . , ϕuk that capture different indicators of proximity:
• The URLs can be aggregated into clusters, and labels URLi can
be replaced by per-cluster binary labels that indicate whether the
user visited some URL from a cluster or not. This reduces the di-
mensionality of the problem, which can be helpful if the number
151152
promotions and advertisements
of available conversion events is relatively small. The distance be-
tween URLs needed for clustering can be calculated based on the
inventory quality scores that are discussed later in this section.
• A conversion can be defined as a visit to the brand’s site, a pur-
chase after an impression, or any purchase.
The brand proximity model can be used to score users at the be-
ginning of a campaign when the actual data about ad responses are
not yet available. The next step will incorporate the new data when
available and adjust the scores.
3.8.3.2 Ad Response Modeling
The goal of the response modeling step is to estimate the conditional
probability of conversion PrpY | u, aq for an ad a. This step basically
does the same thing as the baseline approach described at the begin-
ning of this section – the advertiser uses the proximity model ϕ to
target users at the beginning of the campaign, but, in addition to that,
the ads are shown to a small number of random people to obtain
the desired sampling shown in Figure 3.26. The difference from the
baseline method is that we can now use the outputs of the previous
step as features rather than high-dimensional raw URLs, which makes
the learning process more efficient. Brand proximities can be supple-
mented with additional user information features fu1 , . . . , fur , such as
browser type and geographical location, so the model can be described
as follows:
ψa puq  PrpY | u, aq
 PrpY | ϕu1 , . . . , ϕuk , fu1 , . . . , fur q
(3.57)
The key difference between the models for unconditional proximity
ϕ and conversion propensity ψ is sampling: the family of ϕ models
is constructed to classify users as converted or non-converters regard-
less of the advertisements, whereas the ψ model classifies users as re-
sponders or non-responders and depends on the advertisement. The
scores produced by models ϕ, however, have high predictive power
for response, providing reasonable initial values for ψ and making re-
estimation of ψ more effective as the actual response data arrives.
3.8.3.3
Inventory Quality and Bidding
The final step is to incorporate additional information that is not cap-
tured in the scores produced by the model ψ and to determine the3.8 online advertisements
actual bid price to be submitted to the ad exchange. With the assump-
tion that the ad exchange is a second-price auction, the optimal bid
price can be calculated as the expected value of conversion vpY q:
bopt  E rvpY qs  PrpY | u, aq  vpY q(3.58)
bpuq  bbase  s1 pψa puqq(3.59)
The value of conversion vpY q can typically be assumed to be constant
for all users and is incorporated into some baseline bid price bbase
set by the advertiser and depending on the contract with the brand
and properties of the exchange. Consequently, propensity scores can
be considered as multipliers to scale the baseline price.
Propensity scores produced by the model ψ are generally sufficient
to make targeting and bidding decisions. The bid price for a given user
can be calculated as
in which s1 pq is some scaling function for the score ψ. In particular,
s1 pq can map all scores below a certain threshold to zero (no bidding),
and the threshold can be determined based on the desired number of
impressions and other considerations, as we discussed earlier in the
context of promotions.
The targeting process we have described so far considers the user
profiles and advertisements but not the context of the impression, that
is, the inventory. The quality of the inventory is important for several
reasons [Perlich et al., 2013]:
• The inventory carries information about the user’s purchasing
intent and the relevance of the ad for the user. For example, hotel
advertisements will have higher conversion rates on travel web-
sites than on news sites.
• The perception of an advertisement depends on the context. For
example, users who are reading complex technical materials may
pay less attention to ads than visitors to entertainment sites, some
ad slots may be poorly positioned and require users to scroll
down the page, etc.
Consequently, the advertiser can expect to get better results by using
the probability ωa pu, iq  PrpY | u, a, iq in which i is the inventory.
The ratio ωa pu, iq and its expectation over all inventories ωa puq 
Ei r ωa pu, iq s can be used as a measure of inventory quality because
it shows how much better or worse inventory i is in comparison to an
average inventory. This metric can be used as an additional multiplier
to scale the bid:
bpuq  bbase  s1 pψa puqq  s2

ωa pu, iq
ωa pu q
(3.60)
153154
promotions and advertisements
Note that although the notation we have used implies that ωa puq
equals ψa puq, the advertiser can use different data samples and mod-
els to estimate ω and ψ depending on the available data and other
considerations. The steepness of the scaling functions s1 pq and s2 pq
determines the trade-off between conversion rates and the advertiser’s
CPA. Steep scaling functions (e. g., zero if the argument is below the
threshold and a very high value otherwise) generally maximize the
conversion rate, but these can be suboptimal from the CPA standpoint.
Scaling functions that are close to the identity function optimize the
CPA as it follows from theoretical equation 3.58 but can be suboptimal
in terms of conversion rates.
3.8.4
Multi-Touch Attribution
The obvious limitation of last-touch attribution is that the efforts that
preceded the last impression are neglected. One can work around this
by using more elaborate attribution methods that distribute the credit
according to a position of the advertiser in the funnel. Several exam-
ples of such static models are shown in table 3.9. Static weight-based
attribution, however, does not help to estimate the contribution of in-
dividual advertisers to the overall campaign effect. We need to create
an algorithmic attribution method that measures the actual contributions
and enables the brand to reward the best advertisers or channels and
remove the worst ones.
ModelA1A2A3A4A5
First impression100%––––
First click–100%–––
Last touch––––100%
Linear20%20%20%20%20%
Position-based35%10%10%10%35%
Time decay10%15%20%25%30%
Table 3.9: Static attribution models. The table shows the percentage of credit
assigned to each of five impressions A1 , . . . , A5 .
Let us assume that the brand works with a network of advertisers
or channels C  tC1 , . . . , Cn u. We can think of this network as a set of
states that can be traversed by a user before conversion, as illustrated in
Figure 3.27. We can define the causal effect of channel Ck as the differ-3.8 online advertisements
ence between the probability of conversion for the full set of channels
and the probability of conversion if channel Ck is removed:
Vk  PrpY | Cq  PrpY | CzCk q
(3.61)
To evaluate this expression, we can enumerate all possible subsets of
the set CzCk and estimate the causal effect for each subset separately
[Dalessandro et al., 2012b]:
Vk 
¸
wS,k PrpY | S Y Ck q  PrpY | Sq
 z

(3.62)
S C Ck
Coefficients wS,k model the probability distribution of particular re-
alizations of S, that is, the probability of a user traversing a certain
sequence of channels. By assuming a uniform distribution of all se-
quences, we have
|C|  1 1  1  |S|! p|C|  1  |S|q!
(3.63)
|S|
|C |
|C | !
because we draw sequences of length |S| from the set CzCk with car-
dinality |C|  1. For example, the causal effect of channel C3 in the
network C  tC1 , C2 , C3 u is given by the following equation:
wS,k 
V3 

1
pPrpY | C1 , C2 , C3 q  PrpY | C1 , C2 qq
3
1
pPrpY | C1 , C3 q  PrpY | C1 qq
6

pPrpY | C2 , C3 q  PrpY | C2 qq
1
pPrpY | C3 q  PrpY | ∅qq
3
(3.64)
The attribution formula 3.62 can be difficult to evaluate in prac-
tice because long sequences of channels have relatively low realization
probabilities, which impacts the estimation stability [Dalessandro et al.,
2012b; Shao and Li, 2011]. It can be reasonable to discard all sequences
S longer than 2 channels to produce a more simple and stable model
[Shao and Li, 2011]:
Vk 
¸
wS,k PrpY | S Y Ck q  PrpY | Sq
 z
S C Ck


 w0 PrpY | Ck q  PrpY | ∅q
¸ 

w1
PrpY | Cj , Ck q  PrpY | Cj q

j k

(3.65)
155156
promotions and advertisements
Figure 3.27: Example of a network with three channels.
The baseline probability of conversion PrpY | ∅q can also be dis-
carded because it is equal for all channels, and the coefficients are de-
fined as
|C|  1 1 1  1
| C | |C |
0


1
|C |  1
1
1
w1 
1
|C|  p|C|  1q|C|
w0 

(3.66)
We can therefore express the causal effect as
Vk 
|C| PrpY | Ck q
1
1
¸ 
p|C|  1q|C| jk
PrpY | Cj , Ck q  PrpY | Cj q

(3.67)
The probability of conversion PrpY | Ck q can be estimated as the
ratio of converted users who passed through channel Ck to the total
number of users who passed through the channel. The second-order
probabilities PrpY | Cj , Ck q can be estimated in the same way but for a
pair of channels.
Equations 3.62 and 3.67 describe a practical solution for multi-touch
attribution. However, it is worth noting that there are alternative ways
to approach the same problem. For example, one can build a regres-
sion model that predicts conversions based on traversed channels and
compare the magnitudes of the regression coefficients [Shao and Li,
2011].3.9 measuring the effectiveness
3.9
measuring the effectiveness
The effectiveness of marketing campaigns is inherently challenging to
measure because each consumer has unique properties, changes over
time, and interacts with the brand and marketing media in their own
way, so the attribution of any improvement or degradation to a par-
ticular marketing action can always be debated. Marketers typically
cannot strictly prove the effectiveness of the action, but they can try
to arrange an experiment or analyze the collected data in such a way
that the actions in question and the outcomes are properly isolated, so
that the causal effect cannot be attributed to external factors. This can
be considered as proof of a statistically significant causal relationship
between the actions and outcomes.
This problem statement enables us to leverage a huge statistical the-
ory that was developed in other fields long before algorithmic market-
ing appeared. Importantly, experimentation frameworks developed in
areas such as biology and healthcare are specifically adapted to deal
with scenarios that are structurally similar to marketing campaigns.
Randomized Experiments
3.9.1
Consider a basic marketing campaign that distributes promotions or
advertisements to prospects to make them convert. Although our ulti-
mate goal is to estimate the causal relationship between the treatment
and conversions, we can start with very basic questions and gradually
build a statistical framework that estimates the causal effects.
3.9.1.1
Conversion Rate
One of the most basic questions that we can pose is the measurement
of simple metrics, such as the conversion rate. Based on the assump-
tion that the total number of individuals who received a treatment n
is known and the number of converted individuals k among these n
recipients is measured, we can estimate the conversion rate as
R
k
n
(3.68)
The obtained estimate may or may not be statistically reliable, depend-
ing on the number of individuals and conversions. If these numbers
are small, we can expect the measured rate to have high variance and
to change drastically if the same campaign is run multiple times. If
the numbers are high, we can expect more consistent results. The re-
liability of the estimate can be measured in different ways by using
different statistical frameworks. In this book, we generally advocate
157158
promotions and advertisements
Bayesian methods and Monte Carlo simulations because of their con-
sistency and flexibility, so we use this approach for randomized exper-
iments as well. Although it is not necessarily the most simple solution
for the most basic problems, it helps us to establish a framework that
can be efficiently extended for the more complex scenarios that we will
consider later on.
Because the total number of promotions n is a non-random value
chosen before the experiment, our goal is to understand the distribu-
tion of the conversion rate given the observed number of conversions
ppR | kq. If this distribution is known, we will be able to estimate the
probability that the results of hypothetical repeated experiments would
deviate significantly from the observed value and thus measure the re-
liability of the estimated rate. According to Bayes rule, the distribution
in question can be decomposed as follows:
ppk | RqppRq
p pk q(3.69)
ppk | RqppRqdR(3.70)
ppR | kq 
in which ppk | Rq is the likelihood, that is, the probability, of observing
k conversions given that the conversion rate value is known to be R,
and ppRq is the prior distribution of conversion rates. The probability
ppkq can be viewed as a normalization factor because the data point
k is given; hence, this term just ensures that the rate distribution is a
probability distribution, that is, that the integral over the entire range
is 1. So this value can be expressed as follows:
ppkq 
»
In words, we start with a prior belief about the rate distribution ppRq,
and the observed data, that is, the number of conversions k, provide
evidence for or against our belief. The posterior distribution ppR | kq is
obtained by updating our belief based on the evidence that we see.
As the posterior rate distribution includes two factors, ppk | Rq and
ppRq, we need to specify these two distributions. Under the assumption
that the conversion rate is fixed, the probability that exactly k individ-
uals out of n will convert is given by a binomial distribution, with a
probability mass function of the form
p p k | Rq 

n
k
 Rk p1  Rqnk
 k!pnn! kq!  Rk p1  Rqnk
(3.71)
The second factor, the prior distribution ppRq, can be assumed to
be uniform or can be estimated from historical campaign data. Let us3.9 measuring the effectiveness
consider the case of uniform distribution first. If the prior distribution
ppRq is uniform in the range from 0 to 1, the posterior distribution
ppR | kq has the same form as the likelihood given by equation 3.71,
but it is now a function of R, not k, so the normalizing constant will be
different. We can denote this constant as cpn, kq and obtain
ppR | kq  Rk p1  Rqnk  cpn, kq
(3.72)
This distribution is known as a beta distribution, and there is a stan-
dard notation for it. In this notation, the posterior can be expressed
as
ppR | kq  beta pk
1, n  k
1q
(3.73)
in which the beta distribution is defined as
beta pα, βq 
Bpα, βq 
1
 xα1 p1  xqβ1
Bpα, βq
»1
0
(3.74)
xα1 p1  xqβ1 dx
The distribution of the conversion rate given n treated individuals
and k conversions is described by the beta distribution.
If the prior distribution is not uniform, it can also be modeled as the
beta distribution:
ppRq  beta px, yq
(3.75)
in which parameters x and y can be estimated, for example, based on
historical data. In this case, the posterior distribution is still the beta
distribution:
ppR | kq 9 ppk | Rq  ppRq
9 Rk p1  Rqnk  beta px, yq
9 Rk x1 p1  Rqnk y1
9 beta pk x, n  k yq
(3.76)
It is said that the beta distribution is the conjugate prior to the bi-
nomial distribution: if the likelihood function is binomial, the choice
of a beta prior will ensure that the posterior distribution is also beta.
Note that beta p1, 1q reduces to a uniform distribution, so result 3.73
obtained for the uniform prior is a particular case of expression 3.76.
We can now estimate the probability that the conversion rate R lies
within some credible interval ra, bs as
Prpa
R
bq 
»b
a
beta pk
1, n  k
1q dR
(3.77)
159160
promotions and advertisements
Equation 3.77 can be evaluated analytically, but we can also estimate
the credible interval for a conversion rate by using Monte Carlo simu-
lations. In this case, the estimation process can be described as follows:
1. The inputs are n, k, and the desirable confidence level 0
100%.
q
2. Generate a large number of random values with distribution
beta pk 1, n  k 1q.
3. Estimate the q{2-th and p100  q{2q-th percentiles of the gener-
ated values to obtain the desired credible interval. For example,
we can be 95% confident that the estimate R lies in between the
2.5% and 97.5% percentiles.
Examples of beta distributions for different values of n and k, as well
as the corresponding credible intervals, are shown in Figure 3.28. The
simulation approach can look excessively complicated for the assess-
ment of basic metrics such as the conversion rate, but its advantages
will become more apparent as we move to more complex cases.
p | q
Figure 3.28: Examples of the posterior distribution p R k for the uniform
prior and different sample sizes n. The mean k n
0.1 for all
samples. The vertical lines are the 2.5% and 97.5% percentiles of the
corresponding distributions. We start with the uniform prior, and
the more samples we get, the narrower the posterior distribution
becomes.
3.9.1.2
{ 
Uplift
The conversion rate by itself is not a sufficient measure of the quality of
a targeting algorithm or the effectiveness of a marketing campaign. As3.9 measuring the effectiveness
we discussed earlier in this chapter, the effectiveness is typically mea-
sured as the uplift, which is the difference between conversion rates in
the test and control groups. The conversion rate in the control group
is considered as the baseline, and the uplift can be estimated as the
conversion rate in the test group measured against the baseline rate:
L
R
1
R0
(3.78)
in which R0 is the baseline conversion rate and R is the conversion rate
for the campaign in question. From a statistical standpoint, we also
want to measure the reliability of this estimate, that is, the probability
PrpR ¡ R0 | dataq
(3.79)
to ensure that the obtained results are attributed to the impact of the
campaign in question relative to the baseline, not to some external un-
controlled factors. The standard way to tackle this problem is random-
ized experiments. The approach is to randomly split the consumers who
can potentially be involved in the campaign into two groups (test and
control), provide the test group with the treatment (send promotion,
show ads, present a new website design, etc.), and provide the control
group with the no-action or baseline treatment. Random selection of
test and control individuals is important to ensure that the observed
difference in outcomes is not caused by a systematic bias between the
two groups, such as a difference in average income. Running the test
and control in parallel is also important to ensure equality of the test
conditions for the control groups, which might not be the case, for
example, in a comparison of new data with historical data.
The design of randomized experiments for targeted campaigns is
illustrated by Figure 3.29. The high-propensity customers identified
by the targeting algorithm are divided into test and control groups,
and the test group receives the treatment. The number of positive and
negative outcomes is measured for both groups: nT and nC are the
number of individuals and kT and kC are the number of conversions
in the test and control groups, respectively. The uplift is measured by
comparing the conversion rate of the test group kT {nT with that of the
control group kC {nC .
We now want to assess the probability PrpRT ¡ RC q or, equivalently,
to find a credible interval for uplift L. We can calculate this in a similar
manner to that we used for the credible interval of the conversion rate
in expression 3.77, but now we need to account for the joint distribution
for RT and RC :
Prpa
L
bq 
¼
a L b
LpRT , RC q  PrpRT , RC qdRT dRC
(3.80)
161162
promotions and advertisements
Figure 3.29: Sampling in randomized experiments.
If the randomized experiments are properly designed and executed
to achieve independence between the test and control groups, we can
assume that the joint probability above can be split into individual
distributions of conversion rates:
PrpRT , RC q  PrpRT | kT , nT q  PrpRC | kC , nC q
(3.81)
At this point, we can apply the same simulation approach that we
used for the individual conversion rate. Conversion rates RT and RC
follow the beta distribution, so we can generate the uplift samples by
drawing two conversion rates from the corresponding beta distribu-
tions and calculating the ratio. The process will be as follows:
1. The inputs are values kT , nT , kC , and nC , measured from the
observed data, and the desirable confidence level is 0
q
100%
2. Generate a large number of values L by computing each sample
as follows:
a) Draw RT from the distribution beta pkT
b) Draw RC from the distribution beta pkC
c) Compute L  RT {RC  1
1, nT  kT
1, nC  kC
1q
1q
3. Estimate the desired credible interval for L by taking the q{2th
and p100  q{2qth percentiles for the generated values.
The above approach works for many practical scenarios, for exam-
ple, promotional campaigns, advertisements, and testing of arbitrary
improvements, such as a new design of a website. Randomized ex-
periments, however, impose certain limitations on how a campaign is3.9 measuring the effectiveness
executed, and this can be a problem in some cases. In particular, the
requirement for a control group can incur additional expenses – we
will study this issue in detail in the next section.
It is important to note that measurement of the revenue uplift does
not necessarily require a conversion rate to be measured or even indi-
vidual conversions to be tracked. We just need to know the total rev-
enues generated by the test and control groups over a period of time
after the campaign and estimate the uplift as a ratio between these two
revenue values. This can be the only way to measure the uplift if the
conversion information is not available.
3.9.2
Observational Studies
Randomized experiments can be used in the online advertising en-
vironment to measure the conversion uplift delivered by campaigns.
Randomized methods, however, require one to be very careful with
control group selection to make sure that there is no systematic bias
between the test and control groups. The standard approach to achieve
unbiased randomization is to leave picking of the control users until
the very end of the ad delivery pipeline and to sample the users af-
ter the targeting and bidding stages, as shown in Figure 3.30. The test
users are exposed to the actual ad impressions and the control users
are exposed to some dummy ads, such as public service announce-
ments (PSA), so the uplift between the groups is a measure of the ad
impact.
The presence of an ad exchange, however, introduces a major chal-
lenge because impressions for the control group do not come for free
and have to be purchased, just like the actual impressions. The ques-
tion that arises is whether control group selection can be moved to
before the bidding stage, as shown in Figure 3.31.
This approach effectively means that we do not do a controlled ex-
periment anymore, because the bidding process – which bids are won
and which are lost – is not controlled, and, consequently, it can induce
an arbitrary bias in the test group compared to the control group. We
can only observe bidding outcomes and conversions and measure the
causal effect of the ad by doing statistical inference. This leads us to the
large theory of observational studies and causal inference, which was
under intensive development for decades and is driven by the neces-
sity to analyze processes that are not under the control of researchers.
Our problem with the bidding bias closely matches the problem of
treatment effect under non-compliance in clinical trials. The causal effect
of a treatment can be evaluated by using randomized experiments and
comparing subjects from the test group who received the treatment
163164
promotions and advertisements
Figure 3.30: Uplift estimation in online advertising by using randomized exper-
iments. RT and RC are the conversion rates in the test and control
groups, respectively.
with the control group. Although subjects can be assigned to the test
and control groups randomly, some people in the test group cannot
be exposed to the treatment because of compliance issues. The split
into compliant and non-compliant subgroups after randomization cor-
responds to the win–lose split in the bidding process when it follows
control group selection, so we can leverage the studies dedicated to
clinical trials with non-compliance.
The problem of uplift estimation with observational studies can
be approached by using different techniques. We start with a basic
method that illustrates how some concepts of causality theory can be
applied to the problem [Chalasani and Sriharsha, 2016; Rubin, 1974;
Jo, 2002].
We can see in Figure 3.31 that we have at least three conversion rates
that can be measured directly: RC for the control group, RL
T for the lost
bids in the test group, and RW
T for the users who got actual impressions.
Our goal is to find the conversion rate RW
C , which can be interpreted as
a potential conversion rate of the users who would have been won even
if they were not provided with impressions. This value is hypothetical
because we cannot go into the past, revoke the impressions we already
delivered, and see what would happen. However, it can be estimated3.9 measuring the effectiveness
Figure 3.31: Uplift estimation by using observational studies.
from the known data under certain assumptions. First, we can note
that the ratio γ between the number of users who were won and the
number of users who were lost is directly observable. By assuming that
the distribution of “winners” and “losers” is the same in both test and
control groups, we can claim that
RC  γ  RW
C
p1  γqRLC
(3.82)
L
in which RW
C and RC are the conversion rates that we can expect from
the control users who could be won or lost, respectively, if reassigned
L
to the test group. The second assumption we can make is that RL
C  RT
because both groups contain only “losers” who have not been exposed
to the ad, so we do not expect any bias between them. Consequently,
we can express RW
C by using the known values as follows:
RW
C 
1 
 RC  p1  γqRLT
γ
(3.83)
Finally, the uplift can be estimated as the ratio between the observed
W
RW
T and inferred RC .
165166
promotions and advertisements
The reliability of the uplift estimate can be evaluated by using the
same simulation approach we used for randomized experiments. This
requires us to generate samples according to the uplift distribution,
which can be quite challenging to specify because it is a composition
of several random processes: control group selection, bidding, and con-
versions. We observe only a few bits of information for each realization
of this complex process (assigned group, bidding outcome, and con-
version outcome), but we do not observe the intrinsic properties of the
users and other latent factors that determine the joint probability dis-
tribution of the observed outcomes. In the rest of this section, we will
discuss a statistical framework that combines the idea of potential out-
comes discussed above with advanced simulation methods to infer dis-
tributions of different campaign properties, including, but not limited
to, the uplift [Chickering and Pearl, 1996]. We describe the framework
in two steps. First, we specify the model of the random processes of
interest. Second, we discuss how the model can be evaluated by using
simulations.
3.9.2.1
Model Specification
We can account for the latent factors and their impacts by using the
graphical model presented in Figure 3.32. Each node represents a ran-
dom variable, and the arrows indicate the dependencies between the
nodes. Random variables Z, A, and Y correspond to randomization,
bidding, and conversion. More specifically, binary variable Z P t0, 1u
takes a value of one if the user is assigned to the control group and zero
otherwise, variable A P t0, 1u takes a value of one if we won the bid
and showed the ad and zero otherwise, and, finally, variable Y P t0, 1u
equals one if the user converted and zero otherwise. The random vari-
able S corresponds to the user state and, possibly, other latent factors
that influence the advertiser’s ability to win the bid and get a response
after the impression.
Figure 3.32: Graphical model for an observational study with latent factors.3.9 measuring the effectiveness
At a very high level, we want to understand the joint distribution
Prpz, a, y, sq and integrate over it to obtain a credible interval for the up-
lift L. The question is how to decompose the distribution Prpz, a, y, sq to
make it computationally tractable. The graphical model in Figure 3.32
makes certain assumptions that can be used for decomposition : Z
and S are considered independent because randomization must not
be influenced by external factors, and Z and Y are conditionally inde-
pendent given A and S because conversions can be influenced only
through events A. This leads to the following decomposition of the
probability density:
Prpz, a, y, sq  Prpzq Prpaq Prpa | z, sq Prpy | a, sq
(3.84)
We now need to specify the state random variable S and its role in
the densities Prpa | z, sq and Prpy | a, sq. The idea behind the latent fac-
tors is to capture “the state of the world” that is not observed directly
but can influence outcomes like the uplift. This concept can be consid-
ered as a counterpart of the potential outcomes that we discussed at
the beginning of this section, because if we can infer the state from the
observations then we can evaluate the potential outcomes for different
preconditions. For example, if we know that a given user can never be
won on the exchange, then we can predict the outcomes for assigning
this user to both the test and control groups.
The latent state can be modeled differently depending on the avail-
able data, metrics of interest, and general understanding of the domain.
We use a standard model that illustrates how the latent states can be de-
fined as functions of the observed data and how metrics like uplift can
be derived from the states [Heckerman and Shachter, 1995; Chickering
and Pearl, 1996].
From a campaign efficiency standpoint, we are interested mainly in
two properties of the user: compliance with the advertising method
(ability or inability to win a bid) and response to the advertisement
(converted or not). These properties correspond to the probabilities
Prpa | z, sq and Prpy | a, sq discussed above and can be considered
as the user’s internal state that systematically influences the outcomes
obtained for the user. We can enumerate the possible states separately
for compliance and response and specify a condition for each state that
indicates whether the state is possible for the observed tuple pz, a, yq
or not.
The set of possible user states is a Cartesian product of the
compliance and response behaviors, which gives us a 16-element
167168
promotions and advertisements
ComplianceCondition
C1a
C20
az
C3a
z
C4a
1
Description
User can never see the ad
User sees the ad every time we bid and
only if we bid
User sees the ad if and only if we do not
bid
User always sees the ad
Table 3.10: User compliance states and conditions. States C3 and C4 should
never be the case in the scenario that we consider, but they can occur
in other environments such as omni-channel advertising.
ResponseCondition
R1y
R2
R3
R4
0
ya
ya
y1
Description
User never converts
User converts only after impression
User converts only without impression
User always converts
Table 3.11: User response states and conditions.
set ts1 , . . . , s16 u, in which si iterates through all pairs Cp , Rq
compliance and response behaviors listed in tables 3.10 and 3.11:
S P ts1 , . . . , s16 u

sp 4pq1q  Cp , Rq ,
1 ¤ p, q ¤ 4

of
(3.85)
Consequently, the random variable S is a 16-state random variable
drawn from the set of 16 possible states.

We directly observe binary tuples zj , aj , yj for each user j, but user
states sj are never observed directly. However, if we infer the state, it is
possible to evaluate potential metrics of interest, such as uplift, based
on the inferred states. More specifically, we are interested not in the
individual user states but in a vector of state shares
µ  pµ1 , . . . , µ16 q
(3.86)
in which each share µi is the ratio between the number of users in the
corresponding state si and the total number of observed users. The
metrics can then be defined as functions of µ. For example, the uplift
Lpµq can be defined as the ratio between the sum of the four µi values3.9 measuring the effectiveness
that correspond to states with the R2 response component (and any
compliance component) and the sum of another four µi values that
correspond to the states with the R3 response component. It is possible,
however, to define different functions of µ to answer other questions.
3.9.2.2
Simulation
By assuming the model specified above, we can express the credible
interval of the metric Lpµq via the posterior distribution of the random
vector µ:
Prpa
Lpµq
bq 
»
p q b
Lpµq  ppµ | dataqdµ
(3.87)
a L µ

in which data represents all observed tuples zj , aj , yj . Let us denote
the vector of user states as

s  s1 , . . . , sm
(3.88)
in which m is the number of observed users. The distribution of the
state shares µ can then be considered as a random function of user
states s, which, in turn, are also random variables that are not observed
but are probabilistically inferred from the data. Consequently, we have
to consider the joint distribution of 16 variables in µ and m variables
in s:
Prpa
Lpµq
bq 
»
p q b
Lpµq  ppµ, s | dataqdµds
(3.89)
a L µ
The simulation approach requires the distribution ppµ, s | dataq to
be estimated based on the observed data, so we will be able to draw
vectors µ from this distribution. Once the vectors are generated, it is
possible to calculate samples Lpµq and estimate their distribution. The
question we have to answer now is how to draw samples from the
distribution ppµ, s | dataq for the sake of the simulation. We do not
know the functional form of the distribution, but statistical methods
do exist that can help us with generating samples from the distribution
without specifying it explicitly.
Gibbs sampling is a widely used method of drawing samples
from a multivariate distribution [Geman and Geman, 1984]. Let us
assume that we need to draw samples from a multivariate distribution
ppx1 , . . . , xn q. The Gibbs sampler exploits the fact that this multivariate
distribution can be split into n conditional distributions
ppxi | x1 , . . . , xi1 , xi 1 , . . . , xn q,
1¤i¤n
(3.90)
169170
promotions and advertisements
It can be the case that we cannot sample points directly from the mul-
tivariate distribution, but sampling from the conditional distribution
is possible. The idea in Gibbs sampling is that, rather than probabilis-
tically picking all n variables at once, we can pick one variable at a
time with the remaining variables fixed to their current values. In other
words, each variable is sampled from its conditional distribution with
the remaining variables fixed:
xi  ppxi | x1 , . . . , xi1 , xi 1 , . . . , xn q,
1¤i¤n
(3.91)
This is an iterative algorithm that repeatedly draws samples from the
conditional distributions by substituting previously generated samples
into the conditions. For example, consider the basic case of two vari-
ables x1 and x2 . The variables are first initialized to some values that
can be sampled from the prior distribution and are then updated at
each iteration i according to the following rules:
piq  ppx | xpi1q q
1
2
p
iq
p
i 1 q
x  p px | x
q
x1
2
2
(3.92)
1
This process may need a certain number of iterations to converge, and
then it starts to produce points that follow the distribution ppx1 , x2 q.
This method is very powerful in practice because the conditional dis-
tributions are often much easier to specify than the joint distribution
of interest. A generic version of the Gibbs sampler is provided in algo-
rithm 3.1.

p0 q
p0q from the prior distribution
Initialize x1 , . . . , xn
for iteration i  1, 2, . . . do
piq  p x  xpi1q , xpi1q , . . . , xpi1q
draw x1
1
2
n
3
piq  p x  xpiq , xpi1q , . . . , xpi1q
draw x2
2
1
3
n
...
piq  p x
draw xn
n
 piq piq
 x , x , . . . , xpiq
1
2

n 1
end
Algorithm 3.1: Gibbs sampler.
Let us now come back to the distribution ppµ, s | dataq and inves-
tigate how the Gibbs sampler can be used to draw samples from it.3.9 measuring the effectiveness
As the sampler draws each element of µ and s separately, we can
separately specify the estimation routines for pps | µ, dataq and
ppµ | s, dataq.
For the first probability, we can leverage the assumption that the
users are independent, so the posterior probabilities of the user states
are given by
ppsj  si | µ, s, dataq 9 ppaj , yj | zj , si q  µi
(3.93)
in which ppaj , yj | zj , si q is the likelihood of observing the outcomes
zj , aj , and yj given the state si . We can assume that the likelihood
is equal to one if the observed outcomes agree with the conditions of
state si and zero otherwise. Consequently, the likelihood of state si for
user j can be estimated based on the known values of aj , yj , and zj
and the state conditions from tables 3.10 and 3.11. For a model with 16
states, we estimate a vector of 16 probabilities for each user. This vector
is then multiplied by the prior probability of the state µi , in accordance
with the right-hand side of expression 3.93. The resulting vector of 16
numbers defines the multinomial distribution from which sample sj
can be drawn.
The second part is the conditional distribution ppµ | s, dataq. Let us
denote the number of times state si occurs in s as ni . Because µ is the
vector of state shares, that is, each element µi is the empirical probabil-
ity of state si , the vector of counters ni has a multinomial distribution
with parameter µ. Consequently, the likelihood of observing vector s
given the state shares µ is
¹
i
µn
i
(3.94)
i
and thus the posterior distribution of the state shares is
ppµ | s, dataq 9
¹
i
i
µn
i  Prpµq
(3.95)
The last step is to specify the prior distribution Prpµq. Recall that we
have used a beta distribution for the prior in randomized experiments
because the likelihood had a binomial distribution and the beta distri-
bution is a conjugate prior to the binomial. In a similar way, we now
have a multinomial likelihood and its conjugate prior is the Dirichlet
distribution (see Appendix A): if we choose Prpµq to be the Dirich-
let, the posterior distribution described in expression 3.96 will also be
Dirichlet. More formally, we can express the prior belief as a set of
171172
promotions and advertisements
counters n0i , which are used as parameters of the prior Dirichlet distri-
bution, and the posterior can then be expressed as
ppµ | s, dataq 9
¹
0
0
i
µn
i  Dirpn1 , . . . , n16 q
i
9
¹ n 0 n 1
i
i
(3.96)
µi
i
9 Dirpn01
ni , . . . , n016
n16 q
The above equations can be plugged directly into the Gibbs sampler:
we generate the samples of µ by using expression 3.96, generate m sam-
ples of s by using equation 3.93, and then repeat this process iteratively
until we have enough realizations of vector µ to evaluate the credible
interval of Lpµq.