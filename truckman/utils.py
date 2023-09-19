from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 
import pytz
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils.timezone import localtime

#utilies functions
 

#get request user company
def get_user_company(request):
    if request.user.is_authenticated:
        try:
            company = request.user.company
        except:
            company = None
        return company

#send email 
def send_email(context, template_path, from_name, from_email, subject, recipient_email, replyto_email):
    from_name_email = f'{from_name} <{from_email}>'
    template = render_to_string(template_path, context)
    e_mail = EmailMessage(
        subject,
        template,
        from_name_email, #'John Doe <john.doe@example.com>'
        [recipient_email],
        reply_to=[replyto_email,from_email],
    )
    e_mail.send(fail_silently=False)
#--end

#pdf invoice generator
def generate_invoice_pdf(trip):
    # Create an in-memory buffer to store the PDF
    pdf_buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Set up some basic information on the PDF
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f'Invoice ID: {invoice.invoice_id}')
    c.drawString(100, 730, f'Trip Date: {localtime(trip.date).strftime("%Y-%m-%d %H:%M:%S")}')
    c.drawString(100, 710, f'Customer: {trip.load.estimate.customer.name}')
    c.drawString(100, 690, 'Items:')
    
    # Add invoice line items
    y = 670
    for item in invoice.items.all():
        c.drawString(120, y, f'{item.description}')
        c.drawString(300, y, f'Quantity: {item.quantity}')
        c.drawString(400, y, f'Unit Price: ${item.unit_price}')
        c.drawString(500, y, f'Total: ${item.total}')
        y -= 20
    
    # Add total amount
    c.drawString(100, y - 20, f'Total Amount: ${invoice.total_amount}')

    # Save the PDF content
    c.save()

    # Move the buffer's cursor to the beginning
    pdf_buffer.seek(0)

    return pdf_buffer 

#send email with attachement
def send_email_with_attachment(context, template_path, from_name, from_email, subject, recipient_email, replyto_email, attachment_path):
    # Build the email message
    from_name_email = f'{from_name} <{from_email}>'
    template = render_to_string(template_path, context)
    e_mail = EmailMessage(
        subject,
        template,
        from_name_email,  # 'John Doe <john.doe@example.com>'
        [recipient_email],
        reply_to=[replyto_email, from_email],
    )
    
    # Attach an attachment
    e_mail.attach_file(attachment_path)

    try:
        e_mail.send(fail_silently=False)
    except Exception as e:
        # Handle email sending failure
        print(f"Email sending failed: {str(e)}")
    
#format phone number to 254706384073
def format_phone_number(phone_no, phone_code):
    # Remove any non-digit characters from the phone number
    if phone_no != None:
        phone_no = ''.join(filter(str.isdigit, phone_no))
        #remove plus sign from phone_code
        phone_code = phone_code[1:]
        # Check if the phone number starts with a leading zero
        if phone_no.startswith('0'):
            # Remove the leading zero and prepend phone_code
            phone_no = phone_code + phone_no[1:] 
        else:
            # Otherwise, just prepend phone_code
            phone_no = phone_code + phone_no

        return phone_no  

#deformat the number
def deformat_phone_no(phone_no, phone_code):
    phone_code_length = len(phone_code[1:]) #remove plus sign 
    if phone_no:
        deheaded_phone = phone_no[phone_code_length:] #remove code 700000200
        return deheaded_phone

def user_local_time(user_timezone, datetime_value): 
    # Convert the datetime to the user's timezone
    user_timezone = pytz.timezone(user_timezone)
    user_datetime = datetime_value.astimezone(user_timezone)
    return user_datetime

def to_utc(user_timezone, datetime_value):
    user_timezone = pytz.timezone(user_timezone)
    datetime_local = user_timezone.localize(datetime_value)
    datetime_utc = datetime_local.astimezone(pytz.utc)
    return datetime_utc

phone_codes = [
    ('+93', 'AF +93'),
    ('+355', 'AL +355'),
    ('+213', 'DZ +213'),
    ('+376', 'AD +376'),
    ('+244', 'AO +244'),
    ('+1264', 'AI +1264'),
    ('+672', 'AQ +672'),
    ('+54', 'AR +54'),
    ('+374', 'AM +374'),
    ('+297', 'AW +297'),
    ('+61', 'AU +61'),
    ('+43', 'AT +43'),
    ('+994', 'AZ +994'),
    ('+1242', 'BS +1242'),
    ('+973', 'BH +973'),
    ('+880', 'BD +880'),
    ('+1246', 'BB +1246'),
    ('+375', 'BY +375'),
    ('+32', 'BE +32'),
    ('+501', 'BZ +501'),
    ('+229', 'BJ +229'),
    ('+1441', 'BM +1441'),
    ('+975', 'BT +975'),
    ('+591', 'BO +591'),
    ('+387', 'BA +387'),
    ('+267', 'BW +267'),
    ('+55', 'BR +55'),
    ('+246', 'IO +246'),
    ('+673', 'BN +673'),
    ('+359', 'BG +359'),
    ('+226', 'BF +226'),
    ('+257', 'BI +257'),
    ('+855', 'KH +855'),
    ('+237', 'CM +237'),
    ('+1', 'CA +1'),
    ('+238', 'CV +238'),
    ('+599', 'BQ +599'),
    ('+236', 'CF +236'),
    ('+235', 'TD +235'),
    ('+56', 'CL +56'),
    ('+86', 'CN +86'),
    ('+61', 'CX +61'),
    ('+57', 'CO +57'),
    ('+269', 'KM +269'),
    ('+243', 'CD +243'),
    ('+242', 'CG +242'),
    ('+682', 'CK +682'),
    ('+506', 'CR +506'),
    ('+225', 'CI +225'),
    ('+385', 'HR +385'),
    ('+53', 'CU +53'),
    ('+599', 'CW +599'),
    ('+357', 'CY +357'),
    ('+420', 'CZ +420'),
    ('+45', 'DK +45'),
    ('+253', 'DJ +253'),
    ('+1767', 'DM +1767'),
    ('+1809', 'DO +1809'),
    ('+1829', 'DO +1829'),
    ('+1849', 'DO +1849'),
    ('+593', 'EC +593'),
    ('+20', 'EG +20'),
    ('+503', 'SV +503'),
    ('+240', 'GQ +240'),
    ('+291', 'ER +291'),
    ('+372', 'EE +372'),
    ('+251', 'ET +251'),
    ('+500', 'FK +500'),
    ('+298', 'FO +298'),
    ('+679', 'FJ +679'),
    ('+358', 'FI +358'),
    ('+33', 'FR +33'),
    ('+594', 'GF +594'),
    ('+689', 'PF +689'),
    ('+241', 'GA +241'),
    ('+220', 'GM +220'),
    ('+995', 'GE +995'),
    ('+49', 'DE +49'),
    ('+233', 'GH +233'),
    ('+350', 'GI +350'),
    ('+30', 'GR +30'),
    ('+299', 'GL +299'),
    ('+1473', 'GD +1473'),
    ('+590', 'GP +590'),
    ('+1671', 'GU +1671'),
    ('+502', 'GT +502'),
    ('+44', 'GG +44'),
    ('+224', 'GN +224'),
    ('+245', 'GW +245'),
    ('+592', 'GY +592'),
    ('+509', 'HT +509'),
    ('+379', 'VA +379'),
    ('+504', 'HN +504'),
    ('+852', 'HK +852'),
    ('+36', 'HU +36'),
    ('+354', 'IS +354'),
    ('+91', 'IN +91'),
    ('+62', 'ID +62'),
    ('+98', 'IR +98'),
    ('+964', 'IQ +964'),
    ('+353', 'IE +353'),
    ('+44', 'IM +44'),
    ('+972', 'IL +972'),
    ('+39', 'IT +39'),
    ('+1876', 'JM +1876'),
    ('+81', 'JP +81'),
    ('+44', 'JE +44'),
    ('+962', 'JO +962'),
    ('+7', 'KZ +7'),
    ('+254', 'KE +254'),
    ('+686', 'KI +686'),
    ('+965', 'KW +965'),
    ('+996', 'KG +996'),
    ('+856', 'LA +856'),
    ('+371', 'LV +371'),
    ('+961', 'LB +961'),
    ('+266', 'LS +266'),
    ('+231', 'LR +231'),
    ('+218', 'LY +218'),
    ('+423', 'LI +423'),
    ('+370', 'LT +370'),
    ('+352', 'LU +352'),
    ('+853', 'MO +853'),
    ('+389', 'MK +389'),
    ('+261', 'MG +261'),
    ('+265', 'MW +265'),
    ('+60', 'MY +60'),
    ('+960', 'MV +960'),
    ('+223', 'ML +223'),
    ('+356', 'MT +356'),
    ('+692', 'MH +692'),
    ('+596', 'MQ +596'),
    ('+222', 'MR +222'),
    ('+230', 'MU +230'),
    ('+262', 'YT +262'),
    ('+52', 'MX +52'),
    ('+691', 'FM +691'),
    ('+373', 'MD +373'),
    ('+377', 'MC +377'),
    ('+976', 'MN +976'),
    ('+382', 'ME +382'),
    ('+1664', 'MS +1664'),
    ('+212', 'MA +212'),
    ('+258', 'MZ +258'),
    ('+95', 'MM +95'),
    ('+264', 'NA +264'),
    ('+674', 'NR +674'),
    ('+977', 'NP +977'),
    ('+31', 'NL +31'),
    ('+687', 'NC +687'),
    ('+64', 'NZ +64'),
    ('+505', 'NI +505'),
    ('+227', 'NE +227'),
    ('+234', 'NG +234'),
    ('+683', 'NU +683'),
    ('+672', 'NF +672'),
    ('+850', 'KP +850'),
    ('+1670', 'MP +1670'),
    ('+47', 'NO +47'),
    ('+968', 'OM +968'),
    ('+92', 'PK +92'),
    ('+680', 'PW +680'),
    ('+970', 'PS +970'),
    ('+507', 'PA +507'),
    ('+675', 'PG +675'),
    ('+595', 'PY +595'),
    ('+51', 'PE +51'),
    ('+63', 'PH +63'),
    ('+64', 'PN +64'),
    ('+48', 'PL +48'),
    ('+351', 'PT +351'),
    ('+1787', 'PR +1787'),
    ('+974', 'QA +974'),
    ('+40', 'RO +40'),
    ('+7', 'RU +7'),
    ('+250', 'RW +250'),
    ('+590', 'BL +590'),
    ('+290', 'SH +290'),
    ('+1869', 'KN +1869'),
    ('+1758', 'LC +1758'),
    ('+590', 'MF +590'),
    ('+508', 'PM +508'),
    ('+1784', 'VC +1784'),
    ('+685', 'WS +685'),
    ('+378', 'SM +378'),
    ('+239', 'ST +239'),
    ('+966', 'SA +966'),
    ('+221', 'SN +221'),
    ('+381', 'RS +381'),
    ('+248', 'SC +248'),
    ('+232', 'SL +232'),
    ('+65', 'SG +65'),
    ('+1721', 'SX +1721'),
    ('+421', 'SK +421'),
    ('+386', 'SI +386'),
    ('+677', 'SB +677'),
    ('+252', 'SO +252'),
    ('+27', 'ZA +27'),
    ('+82', 'KR +82'),
    ('+211', 'SS +211'),
    ('+34', 'ES +34'),
    ('+94', 'LK +94'),
    ('+249', 'SD +249'),
    ('+597', 'SR +597'),
    ('+4779', 'SJ +4779'),
    ('+268', 'SZ +268'),
    ('+46', 'SE +46'),
    ('+41', 'CH +41'),
    ('+963', 'SY +963'),
    ('+886', 'TW +886'),
    ('+992', 'TJ +992'),
    ('+255', 'TZ +255'),
    ('+66', 'TH +66'),
    ('+670', 'TL +670'),
    ('+228', 'TG +228'),
    ('+690', 'TK +690'),
    ('+676', 'TO +676'),
    ('+1868', 'TT +1868'),
    ('+216', 'TN +216'),
    ('+90', 'TR +90'),
    ('+993', 'TM +993'),
    ('+1649', 'TC +1649'),
    ('+688', 'TV +688'),
    ('+256', 'UG +256'),
    ('+380', 'UA +380'),
    ('+971', 'AE +971'),
    ('+44', 'GB +44'),
    ('+1', 'US +1'),
    ('+598', 'UY +598'),
    ('+998', 'UZ +998'),
    ('+678', 'VU +678'),
    ('+58', 'VE +58'),
    ('+84', 'VN +84'),
    ('+1284', 'VG +1284'),
    ('+1340', 'VI +1340'),
    ('+681', 'WF +681'),
    ('+967', 'YE +967'),
    ('+260', 'ZM +260'),
    ('+263', 'ZW +263')
]
      