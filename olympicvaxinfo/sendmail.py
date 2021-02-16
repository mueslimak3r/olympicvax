import os

bodylength = 500

def make_mail(sourcename, url, body, timestamp, fromaddr, toaddr):
    subject = "JeffCo Vax - new update from %s" % (sourcename)
    unsubtext = "To unsubscribe from this mailing list, click on this link: [[UNSUB_LINK_LOCALE]]"

    truncated_body = (body[:bodylength - 3] + '...') if len(body) > bodylength else body

    final_body = "new update from %s at %s\n%s\n\nTo read the full update, please visit %s at: %s\nFor more information about this email see: https://jeffcovax.cameronlambert.com\n\n\n\n\n%s" % (sourcename, timestamp, truncated_body, sourcename, url, unsubtext)

    command = "echo '%s' | mailx -r %s -s '%s' %s" % (final_body, fromaddr, subject, toaddr)
    return (command)

def sendmail(sourcename, url, body, timestamp):
    command = make_mail(sourcename, url, body, timestamp, 'jeffcovax@cameronlambert.com', 'xntl5lpu1@lists.mailjet.com')
    print("sending mail to mailing list")
    print (command)
    os.system(command)

def testmail(sourcename, url, body, timestamp):
    command = make_mail(sourcename, url, body, timestamp, 'jeffcovax@cameronlambert.com', 'cameronlambert98@gmail.com')
    print("sending test mail")
    print (command)
    os.system(command)

thing = 'Jefferson Healthcare is public hospital located in Port Townsend, Washington \
This page was last updated 02/15/2021 at 1:55 pm \
Vaccination Update, Friday, February 12, 2021 \
Vaccine Supply: \
We have vaccine! \
This morning (Friday, 2/12) we were informed that our orders for 200 Moderna second/booster dose vaccines AND 975 Pfizer first/primary dose vaccines were approved. Inclement weather has complicated shipping, so we have been told to expect delivery Tuesday, February 16. We will operate the immunization clinic this coming Wednesday, Thursday, Friday, and the following Monday to assure all Pfizer 1st dose/booster shots are delivered as quickly as possible. The Moderna vaccine supply is designated for 2nd/booster dose shots and will be used to fill prescheduled 2nd dose vaccinations. \
Read More \
We have heard from many of you that our system of pushing out vaccine availability emails to the entire community when only a few appointments are available sets off a mad scramble to our JOT scheduling system and creates in the words of one resident, a “Black Friday Sale shopping like frenzy” for those seeking vaccinations. We agree; this is not the fairest and most reasonable way to allocate vaccines. \
Next week’s appointments will be targeted at the oldest and frailest in our community. Accordingly, we plan to pull in, starting at the top of the list and in descending order of age, the oldest residents of our community who have registered through the  “When is it my turn” link on our site, which is now over 7000 patients long. \
The vaccine email will include a scheduling link to our JOT registration system and we will allow 48 hours for the recipient to accept the invitation and schedule directly on our JOT system. This approach accomplishes many things; first, it maintains our commitment to vaccinating the oldest, frailest, and most vulnerable residents first. Second, it removes the anxiety and stampede like urgency triggered when we announce vaccine is available. And third, it reassures all residents that when you register for “When is it my turn” there is a fair-minded and methodical system in place. Simply put, once registered, there is one primary line, it is moving and you’re in it.\
In addition, we will continue to target our most clinically frail by identifying a minor portion of vaccine from each allotment for the most clinically frail and vulnerable, as defined by the CDC and Jefferson Healthcare medical staff leadership, and a minor portion of vaccine to reach out to communities who have been left behind and are also most vulnerable to the ravages of COVID-19. While these two cohorts represent a very small portion of the vaccine supply, it is important that we be transparent about our commitment to an equitable vaccine delivery system and how we intend to act on this commitment. \
Vaccine Supply/Demand Imbalance: \
Wednesday, we shared the imbalance of the supply and demand on a state level (446,750 doses ordered by the state and only 206,125 confirmed from the federal government). And Thursday, we received additional information from DOH of the rebalancing of first and second doses for next week. Data shows there are currently more people due for second doses than anticipated in Washington since some second-dose stock was given out as first doses over the past month. \
To correct for this, DOH will prioritize second-dose orders next week for the entire state. The hope is that this is enough of a course correction and going forward this would put the entire state back into alignment on first and second doses for each order. Given this information, we were especially pleased to receive notice of allocation for Pfizer first dose/primary shots. \
Vaccine Clinic: \
The Drive-Thru Immunization Clinic will complete second dose/booster vaccinations late Friday afternoon. As of the end of day Thursday, we have provided 6,492 total vaccinations and completed 2,983 two dose regimens, representing 11% of our population completing the series. \
Vaccine Supply Assessment: \
Information at the state level discusses new allocation plans which would allow for better future planning. This would provide predictability for our organization as well as provide a much needed line of sight on vaccine availability for our community. We will keep you informed of these changes when we learn more.'

if __name__ == '__main__':
    testmail("jeffersonhealthcare", "https://jeffersonhealthcare.org/covid-19-vaccine/", thing, '13:26:11 02/14/21 PST')
