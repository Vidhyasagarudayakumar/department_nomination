
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import nominationform
from .models import nomination
import csv
from django.utils.encoding import smart_str
import yagmail

yagmail.register('da.nomination@kct.ac.in', 'Leadership')

def nominationfields(request):
    form = nominationform()
    if request.method == "POST":
        form = nominationform(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile_No']
            if len(mobile) > 10 or len(mobile) < 10:
                errors = 1
                return render(request, 'nomination_templates/nominationform.html', {'form': form, 'error': errors})
            else:
                nomi = form.save()
                success = 1
                usermail = nomi.email_id
                sendmail(usermail)
                queryset = nomination.objects.filter(rollno=nomi.rollno).order_by('-applied_at')[0]
                form = nominationform()
                return render(request, 'nomination_templates/nominationform.html',
                              {'success': success, 'form': form, 'id': queryset.id})
    return render(request, 'nomination_templates/nominationform.html', {'form': form})


@login_required
def profile(request, pk):
    form = nomination.objects.get(id=pk)
    return render(request, 'nomination_templates/profile.html', {'form': form})


@login_required
def registration(request):
    form = nomination.objects.all()
    count_president = form.filter(req_posistion='President').count()
    count_treasurer = form.filter(req_posistion='Treasurer').count()
    count_secretary = form.filter(req_posistion='Secretary').count()
    count_joint = form.filter(req_posistion='Joint Secretary').count()

    return render(request, 'nomination_templates/registration.html',
                  {'form': form, 'cp': count_president, 'cs': count_secretary, 'cj': count_joint,
                   'ct': count_treasurer})


@login_required
def presidentview(request):
    form = nomination.objects.filter(req_posistion='President')
    return render(request, 'nomination_templates/participant.html', {'form': form})


@login_required
def treasurerview(request):
    form = nomination.objects.filter(req_posistion='Treasurer')
    return render(request, 'nomination_templates/participant.html', {'form': form})


@login_required
def secretaryview(request):
    form = nomination.objects.filter(req_posistion='Secretary')
    return render(request, 'nomination_templates/participant.html', {'form': form})


@login_required
def jointsecretaryview(request):
    form = nomination.objects.filter(req_posistion='Joint Secretary')
    return render(request, 'nomination_templates/participant.html', {'form': form})


@login_required
def download(request):
    return render(request, 'nomination_templates/download.html')


@login_required
def export_csv(request):
    form = nomination.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=nominations.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Refernce Id"),
        smart_str(u"Roll No"),
        smart_str(u"Name"),
        smart_str(u"Gender"),
        smart_str(u"Year"),
        smart_str(u"Quota"),
        smart_str(u"Branch"),
        smart_str(u"CGPA"),
        smart_str(u"No of Arrears"),
        smart_str(u"Area of Residence"),
        smart_str(u"Type of Entry"),
        smart_str(u"Disciplinary Action Faced?"),
        smart_str(u"Mobile Number"),
        smart_str(u"Email"),
        smart_str(u"Position Applied"),
        smart_str(u"Things to be Implemented or Changed, If selected "),
        smart_str(u"Strengths"),
        smart_str(u"Reference Faculty 1	"),
        smart_str(u"Reference Faculty 2"),
        smart_str(u"Name of the Class Advisor"),

    ])
    for obj in form:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.rollno),
            smart_str(obj.name),
            smart_str(obj.gender),
            smart_str(obj.year),
            smart_str(obj.admission_type),
            smart_str(obj.branch),
            smart_str(obj.cgpa),
            smart_str(obj.history_of_arrears),
            smart_str(obj.no_of_arrears),
            smart_str(obj.area_of_residence),
            smart_str(obj.type_of_entry),
            smart_str(obj.faced_disciplinary_action),
            smart_str(obj.mobile_No),
            smart_str(obj.email_id),
            smart_str(obj.req_posistion),
            smart_str(obj.change_in_dept),
            smart_str(obj.strengths),
            smart_str(obj.reference1),
            smart_str(obj.reference2),
            smart_str(obj.class_advisor),
            smart_str(obj.applied_at),

        ])
    return response


export_csv.short_description = u"Export CSV"


def signout(request):
    logout(request)
    return redirect('login')


def sendmail(usermail):
    yag = yagmail.SMTP('da.nomination@kct.ac.in')
    to = str(usermail)
    subject = 'KCT DA | Nominations'
    body = ''
    html = '<!doctype html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head><!--[if gte mso 15]><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]--><meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1"><title>*|MC:SUBJECT|*</title> <style type="text/css">p{margin:10px 0;padding:0;}table{border-collapse:collapse;}h1,h2,h3,h4,h5,h6{display:block;margin:0;padding:0;}img,a img{border:0;height:auto;outline:none;text-decoration:none;}body,#bodyTable,#bodyCell{height:100%;margin:0;padding:0;width:100%;}#outlook a{padding:0;}img{-ms-interpolation-mode:bicubic;}table{mso-table-lspace:0pt;mso-table-rspace:0pt;}.ReadMsgBody{width:100%;}.ExternalClass{width:100%;}p,a,li,td,blockquote{mso-line-height-rule:exactly;}a[href^=tel],a[href^=sms]{color:inherit;cursor:default;text-decoration:none;}p,a,li,td,body,table,blockquote{-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%;}.ExternalClass,.ExternalClass p,.ExternalClass td,.ExternalClass div,.ExternalClass span,.ExternalClass font{line-height:100%;}a[x-apple-data-detectors]{color:inherit !important;text-decoration:none !important;font-size:inherit !important;font-family:inherit !important;font-weight:inherit !important;line-height:inherit !important;}#bodyCell{padding:10px;}.templateContainer{max-width:600px !important;}a.mcnButton{display:block;}.mcnImage{vertical-align:bottom;}.mcnTextContent{word-break:break-word;}.mcnTextContent img{height:auto !important;}.mcnDividerBlock{table-layout:fixed !important;}/*@tab Page@section Background Style@tip Set the background color and top border for your email. You may want to choose colors that match your companys branding.*/body,#bodyTable{/*@editable*/background-color:#FAFAFA;}/*@tab Page@section Background Style@tip Set the background color and top border for your email. You may want to choose colors that match your companys branding.*/#bodyCell{/*@editable*/border-top:0;}/*@tab Page@section Email Border@tip Set the border for your email.*/.templateContainer{/*@editable*/border:0;}/*@tab Page@section Heading 1@tip Set the styling for all first-level headings in your emails. These should be the largest of your headings.@style heading 1*/h1{/*@editable*/color:#202020;/*@editable*/font-family:Helvetica;/*@editable*/font-size:26px;/*@editable*/font-style:normal;/*@editable*/font-weight:bold;/*@editable*/line-height:125%;/*@editable*/letter-spacing:normal;/*@editable*/text-align:left;}/*@tab Page@section Heading 2@tip Set the styling for all second-level headings in your emails.@style heading 2*/h2{/*@editable*/color:#202020;/*@editable*/font-family:Helvetica;/*@editable*/font-size:22px;/*@editable*/font-style:normal;/*@editable*/font-weight:bold;/*@editable*/line-height:125%;/*@editable*/letter-spacing:normal;/*@editable*/text-align:left;}/*@tab Page@section Heading 3@tip Set the styling for all third-level headings in your emails.@style heading 3*/h3{/*@editable*/color:#202020;/*@editable*/font-family:Helvetica;/*@editable*/font-size:20px;/*@editable*/font-style:normal;/*@editable*/font-weight:bold;/*@editable*/line-height:125%;/*@editable*/letter-spacing:normal;/*@editable*/text-align:left;}/*@tab Page@section Heading 4@tip Set the styling for all fourth-level headings in your emails. These should be the smallest of your headings.@style heading 4*/h4{/*@editable*/color:#202020;/*@editable*/font-family:Helvetica;/*@editable*/font-size:18px;/*@editable*/font-style:normal;/*@editable*/font-weight:bold;/*@editable*/line-height:125%;/*@editable*/letter-spacing:normal;/*@editable*/text-align:left;}/*@tab Preheader@section Preheader Style@tip Set the background color and borders for your emails preheader area.*/#templatePreheader{/*@editable*/background-color:#fafafa;/*@editable*/background-image:none;/*@editable*/background-repeat:no-repeat;/*@editable*/background-position:center;/*@editable*/background-size:cover;/*@editable*/border-top:0;/*@editable*/border-bottom:0;/*@editable*/padding-top:9px;/*@editable*/padding-bottom:9px;}/*@tab Preheader@section Preheader Text@tip Set the styling for your emails preheader text. Choose a size and color that is easy to read.*/#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{/*@editable*/color:#656565;/*@editable*/font-family:Helvetica;/*@editable*/font-size:12px;/*@editable*/line-height:150%;/*@editable*/text-align:left;}/*@tab Preheader@section Preheader Link@tip Set the styling for your emails preheader links. Choose a color that helps them stand out from your text.*/#templatePreheader .mcnTextContent a,#templatePreheader .mcnTextContent p a{/*@editable*/color:#656565;/*@editable*/font-weight:normal;/*@editable*/text-decoration:underline;}/*@tab Header@section Header Style@tip Set the background color and borders for your emails header area.*/#templateHeader{/*@editable*/background-color:#FFFFFF;/*@editable*/background-image:none;/*@editable*/background-repeat:no-repeat;/*@editable*/background-position:center;/*@editable*/background-size:cover;/*@editable*/border-top:0;/*@editable*/border-bottom:0;/*@editable*/padding-top:9px;/*@editable*/padding-bottom:0;}/*@tab Header@section Header Text@tip Set the styling for your emails header text. Choose a size and color that is easy to read.*/#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{/*@editable*/color:#202020;/*@editable*/font-family:Helvetica;/*@editable*/font-size:16px;/*@editable*/line-height:150%;/*@editable*/text-align:left;}/*@tab Header@section Header Link@tip Set the styling for your emails header links. Choose a color that helps them stand out from your text.*/#templateHeader .mcnTextContent a,#templateHeader .mcnTextContent p a{/*@editable*/color:#2BAADF;/*@editable*/font-weight:normal;/*@editable*/text-decoration:underline;}/*@tab Body@section Body Style@tip Set the background color and borders for your emails body area.*/#templateBody{/*@editable*/background-color:#FFFFFF;/*@editable*/background-image:none;/*@editable*/background-repeat:no-repeat;/*@editable*/background-position:center;/*@editable*/background-size:cover;/*@editable*/border-top:0;/*@editable*/border-bottom:2px solid #EAEAEA;/*@editable*/padding-top:0;/*@editable*/padding-bottom:9px;}/*@tab Body@section Body Text@tip Set the styling for your emails body text. Choose a size and color that is easy to read.*/#templateBody .mcnTextContent,#templateBody .mcnTextContent p{/*@editable*/color:#202020;/*@editable*/font-family:Helvetica;/*@editable*/font-size:16px;/*@editable*/line-height:150%;/*@editable*/text-align:left;}/*@tab Body@section Body Link@tip Set the styling for your emails body links. Choose a color that helps them stand out from your text.*/#templateBody .mcnTextContent a,#templateBody .mcnTextContent p a{/*@editable*/color:#2BAADF;/*@editable*/font-weight:normal;/*@editable*/text-decoration:underline;}/*@tab Footer@section Footer Style@tip Set the background color and borders for your emails footer area.*/#templateFooter{/*@editable*/background-color:#FAFAFA;/*@editable*/background-image:none;/*@editable*/background-repeat:no-repeat;/*@editable*/background-position:center;/*@editable*/background-size:cover;/*@editable*/border-top:0;/*@editable*/border-bottom:0;/*@editable*/padding-top:9px;/*@editable*/padding-bottom:9px;}/*@tab Footer@section Footer Text@tip Set the styling for your emails footer text. Choose a size and color that is easy to read.*/#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{/*@editable*/color:#656565;/*@editable*/font-family:Helvetica;/*@editable*/font-size:12px;/*@editable*/line-height:150%;/*@editable*/text-align:center;}/*@tab Footer@section Footer Link@tip Set the styling for your emails footer links. Choose a color that helps them stand out from your text.*/#templateFooter .mcnTextContent a,#templateFooter .mcnTextContent p a{/*@editable*/color:#656565;/*@editable*/font-weight:normal;/*@editable*/text-decoration:underline;}@media only screen and (min-width:768px){.templateContainer{width:600px !important;}}@media only screen and (max-width: 480px){body,table,td,p,a,li,blockquote{-webkit-text-size-adjust:none !important;}}@media only screen and (max-width: 480px){body{width:100% !important;min-width:100% !important;}}@media only screen and (max-width: 480px){#bodyCell{padding-top:10px !important;}}@media only screen and (max-width: 480px){.mcnImage{width:100% !important;}}@media only screen and (max-width: 480px){.mcnCartContainer,.mcnCaptionTopContent,.mcnRecContentContainer,.mcnCaptionBottomContent,.mcnTextContentContainer,.mcnBoxedTextContentContainer,.mcnImageGroupContentContainer,.mcnCaptionLeftTextContentContainer,.mcnCaptionRightTextContentContainer,.mcnCaptionLeftImageContentContainer,.mcnCaptionRightImageContentContainer,.mcnImageCardLeftTextContentContainer,.mcnImageCardRightTextContentContainer{max-width:100% !important;width:100% !important;}}@media only screen and (max-width: 480px){.mcnBoxedTextContentContainer{min-width:100% !important;}}@media only screen and (max-width: 480px){.mcnImageGroupContent{padding:9px !important;}}@media only screen and (max-width: 480px){.mcnCaptionLeftContentOuter .mcnTextContent,.mcnCaptionRightContentOuter .mcnTextContent{padding-top:9px !important;}}@media only screen and (max-width: 480px){.mcnImageCardTopImageContent,.mcnCaptionBlockInner .mcnCaptionTopContent:last-child .mcnTextContent{padding-top:18px !important;}}@media only screen and (max-width: 480px){.mcnImageCardBottomImageContent{padding-bottom:9px !important;}}@media only screen and (max-width: 480px){.mcnImageGroupBlockInner{padding-top:0 !important;padding-bottom:0 !important;}}@media only screen and (max-width: 480px){.mcnImageGroupBlockOuter{padding-top:9px !important;padding-bottom:9px !important;}}@media only screen and (max-width: 480px){.mcnTextContent,.mcnBoxedTextContentColumn{padding-right:18px !important;padding-left:18px !important;}}@media only screen and (max-width: 480px){.mcnImageCardLeftImageContent,.mcnImageCardRightImageContent{padding-right:18px !important;padding-bottom:0 !important;padding-left:18px !important;}}@media only screen and (max-width: 480px){.mcpreview-image-uploader{display:none !important;width:100% !important;}}@media only screen and (max-width: 480px){/*@tab Mobile Styles@section Heading 1@tip Make the first-level headings larger in size for better readability on small screens.*/h1{/*@editable*/font-size:22px !important;/*@editable*/line-height:125% !important;}}@media only screen and (max-width: 480px){/*@tab Mobile Styles@section Heading 2@tip Make the second-level headings larger in size for better readability on small screens.*/h2{/*@editable*/font-size:20px !important;/*@editable*/line-height:125% !important;}}@media only screen and (max-width: 480px){/*@tab Mobile Styles@section Heading 3@tip Make the third-level headings larger in size for better readability on small screens.*/h3{/*@editable*/font-size:18px !important;/*@editable*/line-height:125% !important;}}@media only screen and (max-width: 480px){/*@tab Mobile Styles@section Heading 4@tip Make the fourth-level headings larger in size for better readability on small screens.*/h4{/*@editable*/font-size:16px !important;/*@editable*/line-height:150% !important;}}@media only screen and (max-width: 480px){/*@tab Mobile Styles@section Boxed Text@tip Make the boxed text larger in size for better readability on small screens. We recommend a font size of at least 16px.*/.mcnBoxedTextContentContainer .mcnTextContent,.mcnBoxedTextContentContainer .mcnTextContent p{/*@editable*/font-size:14px !important;/*@editable*/line-height:150% !important;}}@media only screen and (max-width: 480px){/*@tab Mobile Styles@section Preheader Visibility@tip Set the visibility of the emails preheader on small screens. You can hide it to save space.*/#templatePreheader{/*@editable*/display:block !important;}}@media only screen and (max-width: 480px){/*@tab Mobile Styles@section Preheader Text@tip Make the preheader text larger in size for better readability on small screens.*/#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{/*@editable*/font-size:14px !important;/*@editable*/line-height:150% !important;}}@media only screen and (max-width: 480px){/*@tab Mobile Styles@section Header Text@tip Make the header text larger in size for better readability on small screens.*/#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{/*@editable*/font-size:16px !important;/*@editable*/line-height:150% !important;}}@media only screen and (max-width: 480px){/*@tab Mobile Styles@section Body Text@tip Make the body text larger in size for better readability on small screens. We recommend a font size of at least 16px.*/#templateBody .mcnTextContent,#templateBody .mcnTextContent p{/*@editable*/font-size:16px !important;/*@editable*/line-height:150% !important;}}@media only screen and (max-width: 480px){/*@tab Mobile Styles@section Footer Text@tip Make the footer content text larger in size for better readability on small screens.*/#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{/*@editable*/font-size:14px !important;/*@editable*/line-height:150% !important;}}</style></head> <body> <center> <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable"> <tr> <td align="center" valign="top" id="bodyCell"><!--[if gte mso 9]><table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;"><tr><td align="center" valign="top" width="600" style="width:600px;"><![endif]--> <table border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer"> <tr> <td valign="top" id="templatePreheader"></td></tr><tr> <td valign="top" id="templateHeader"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageBlock" style="min-width:100%;"> <tbody class="mcnImageBlockOuter"> <tr> <td valign="top" style="padding:9px" class="mcnImageBlockInner"> <table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer" style="min-width:100%;"> <tbody><tr> <td class="mcnImageContent" valign="top" style="padding-right: 9px; padding-left: 9px; padding-top: 0; padding-bottom: 0; text-align:center;"> <img align="center" alt="" src="https://gallery.mailchimp.com/c70570c9a27fae436f2b070b6/images/919d7864-1e0c-460a-8896-12dad5e25676.png" width="564" style="max-width:1872px; padding-bottom: 0; display: inline !important; vertical-align: bottom;" class="mcnImage"> </td></tr></tbody></table> </td></tr></tbody></table></td></tr><tr> <td valign="top" id="templateBody"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnBoxedTextBlock" style="min-width:100%;"><!--[if gte mso 9]><table align="center" border="0" cellspacing="0" cellpadding="0" width="100%"><![endif]--><tbody class="mcnBoxedTextBlockOuter"> <tr> <td valign="top" class="mcnBoxedTextBlockInner"><!--[if gte mso 9]><td align="center" valign="top" "><![endif]--> <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;" class="mcnBoxedTextContentContainer"> <tbody><tr> <td style="padding-top:9px; padding-left:18px; padding-bottom:9px; padding-right:18px;"> <table border="0" cellpadding="18" cellspacing="0" class="mcnTextContentContainer" width="100%" style="min-width: 100% !important;background-color: #212F45;"> <tbody><tr> <td valign="top" class="mcnTextContent" style="color: #F2F2F2;font-family: Helvetica;font-size: 14px;font-weight: normal;text-align: center;"> <div style="text-align: center;"><u>Nomination for Department Association - <strong>President</strong></u></div><div style="text-align: justify;"><br>We are glad to share the department association president selection procedure for the academic year 2017-18. Students are encouraged to apply for the leadership positions in the Department Association and work for enhancement of the department through various measures. Interested Students are requested to apply through the online application form available at the KCT Website. The last date to apply is March 18, 2017.</div>&nbsp;<div style="text-align: left;"><strong><u>Roles and Responsibilities</u></strong></div><ul><li style="text-align: justify;">Will plan the activities jointly with office bearers and interface with the HoD, Faculty and Staff.</li><li style="text-align: justify;">Will sign letter and communications on behalf of the departmental association.</li><li style="text-align: justify;">Will lead the Department in developing and implementing immediate and long range departmental goals and activities.</li><li style="text-align: justify;">Will lead the department in promoting inter-departmental cooperation and interdisciplinary initiatives.</li><li style="text-align: justify;">Will chair the Department Association monthly meeting.</li><li style="text-align: justify;">Will represent his/her Department at official college function.</li></ul><div style="text-align: justify;"><div style="text-align: left;"><strong><u>Selection Process</u></strong></div><ul><li>Students with not more than two standing arrears and no involvement in any indiscipline activities are eligible to apply.</li><li>Registration will be considered only with the Letter of Recommendation from three Faculty Members, submitted to the current Department Association President / Vice President / Treasurer / Faculty In-Charge.</li><li>A PPT presentation with two slides containing personal information and plans for the association.</li><li>Panel consisting of JC, Principal / PMO / Director - KCTBS, OSA, HoD, Senior faculty, middle level faculty, alumni, LC Members and other department faculty will select the President, using the rubric as given below.<ul style="list-style-type:circle;"><li>Academic : 30 %</li><li>Co-curricular and Extra-curricular : 30 %</li><li>Plan for the association : 40 %</li></ul></li></ul>The sub-division for the rubric are subjective to changes.</div></td></tr></tbody></table> </td></tr></tbody></table><!--[if gte mso 9]></td><![endif]--><!--[if gte mso 9]> </tr></table><![endif]--> </td></tr></tbody></table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnButtonBlock" style="min-width:100%;"> <tbody class="mcnButtonBlockOuter"> <tr> <td style="padding-top:0; padding-right:18px; padding-bottom:18px; padding-left:18px;" valign="top" align="center" class="mcnButtonBlockInner"> <table border="0" cellpadding="0" cellspacing="0" class="mcnButtonContentContainer" style="border-collapse: separate !important;border-top-left-radius: 3px;border-top-right-radius: 3px;border-bottom-right-radius: 3px;border-bottom-left-radius: 3px;background-color: #2BAADF;"> <tbody> <tr> <td align="center" valign="middle" class="mcnButtonContent" style="font-family: Arial; font-size: 16px; padding: 15px;"> <a class="mcnButton " title="Click Here to Download - PPT Format" href="http://" target="_blank" style="font-weight: bold;letter-spacing: normal;line-height: 100%;text-align: center;text-decoration: none;color: #FFFFFF;">Click Here to Download - PPT Format</a> </td></tr></tbody> </table> </td></tr></tbody></table></td></tr><tr> <td valign="top" id="templateFooter"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowBlock" style="min-width:100%;"> <tbody class="mcnFollowBlockOuter"> <tr> <td align="center" valign="top" style="padding:9px" class="mcnFollowBlockInner"> <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentContainer" style="min-width:100%;"> <tbody><tr> <td align="center" style="padding-left:9px;padding-right:9px;"> <table border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;" class="mcnFollowContent"> <tbody><tr> <td align="center" valign="top" style="padding-top:9px; padding-right:9px; padding-left:9px;"> <table align="center" border="0" cellpadding="0" cellspacing="0"> <tbody><tr> <td align="center" valign="top"><!--[if mso]> <table align="center" border="0" cellspacing="0" cellpadding="0"> <tr><![endif]--><!--[if mso]> <td align="center" valign="top"><![endif]--> <table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;"> <tbody><tr> <td valign="top" style="padding-right:10px; padding-bottom:9px;" class="mcnFollowContentItemContainer"> <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem"> <tbody><tr> <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;"> <table align="left" border="0" cellpadding="0" cellspacing="0" width=""> <tbody><tr> <td align="center" valign="middle" width="24" class="mcnFollowIconContent"> <a href="http://www.youtube.com/channel/UCQ71Y6dp5f-HZaKB4ZQZDlg" target="_blank"><img src="https://cdn-images.mailchimp.com/icons/social-block-v2/color-youtube-48.png" style="display:block;" height="24" width="24" class=""></a> </td></tr></tbody></table> </td></tr></tbody></table> </td></tr></tbody></table><!--[if mso]> </td><![endif]--><!--[if mso]> <td align="center" valign="top"><![endif]--> <table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;"> <tbody><tr> <td valign="top" style="padding-right:10px; padding-bottom:9px;" class="mcnFollowContentItemContainer"> <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem"> <tbody><tr> <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;"> <table align="left" border="0" cellpadding="0" cellspacing="0" width=""> <tbody><tr> <td align="center" valign="middle" width="24" class="mcnFollowIconContent"> <a href="https://www.facebook.com/KCT.edu" target="_blank"><img src="https://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-48.png" style="display:block;" height="24" width="24" class=""></a> </td></tr></tbody></table> </td></tr></tbody></table> </td></tr></tbody></table><!--[if mso]> </td><![endif]--><!--[if mso]> <td align="center" valign="top"><![endif]--> <table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;"> <tbody><tr> <td valign="top" style="padding-right:10px; padding-bottom:9px;" class="mcnFollowContentItemContainer"> <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem"> <tbody><tr> <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;"> <table align="left" border="0" cellpadding="0" cellspacing="0" width=""> <tbody><tr> <td align="center" valign="middle" width="24" class="mcnFollowIconContent"> <a href="http://www.kct.ac.in" target="_blank"><img src="https://cdn-images.mailchimp.com/icons/social-block-v2/color-link-48.png" style="display:block;" height="24" width="24" class=""></a> </td></tr></tbody></table> </td></tr></tbody></table> </td></tr></tbody></table><!--[if mso]> </td><![endif]--><!--[if mso]> <td align="center" valign="top"><![endif]--> <table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;"> <tbody><tr> <td valign="top" style="padding-right:0; padding-bottom:9px;" class="mcnFollowContentItemContainer"> <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem"> <tbody><tr> <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;"> <table align="left" border="0" cellpadding="0" cellspacing="0" width=""> <tbody><tr> <td align="center" valign="middle" width="24" class="mcnFollowIconContent"> <a href="mailto:vijilesh@kct.ac.in" target="_blank"><img src="https://cdn-images.mailchimp.com/icons/social-block-v2/color-forwardtofriend-48.png" style="display:block;" height="24" width="24" class=""></a> </td></tr></tbody></table> </td></tr></tbody></table> </td></tr></tbody></table><!--[if mso]> </td><![endif]--><!--[if mso]> </tr></table><![endif]--> </td></tr></tbody></table> </td></tr></tbody></table> </td></tr></tbody></table> </td></tr></tbody></table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnDividerBlock" style="min-width:100%;"> <tbody class="mcnDividerBlockOuter"> <tr> <td class="mcnDividerBlockInner" style="min-width: 100%; padding: 10px 18px 25px;"> <table class="mcnDividerContent" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%;border-top-width: 2px;border-top-style: solid;border-top-color: #EEEEEE;"> <tbody><tr> <td> <span></span> </td></tr></tbody></table><!-- <td class="mcnDividerBlockInner" style="padding: 18px;"> <hr class="mcnDividerContent" style="border-bottom-color:none; border-left-color:none; border-right-color:none; border-bottom-width:0; border-left-width:0; border-right-width:0; margin-top:0; margin-right:0; margin-bottom:0; margin-left:0;"/>--> </td></tr></tbody></table></td></tr></table><!--[if gte mso 9]></td></tr></table><![endif]--> </td></tr></table> </center> </body></html>'
    yag.send(to=to, subject=subject, contents=[body, html])
