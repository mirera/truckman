#send all trip document to shipper
@login_required(login_url='login')
@permission_required('trip.view_trip')
def send_to_shipper(request, pk):
    company = get_user_company(request)
    trip = Trip.objects.get(id=pk, company=company)
    shipper = trip.load.shipper
    vehicle = trip.vehicle
    driver = Driver.objects.get(assigned_vehicle=vehicle)

    # Create a PDF file with all trip documents
    merger = PdfMerger()

    all_trip_documents = [
        trip.vehicle.truck_logbook,
        trip.vehicle.trailer_logbook,
        trip.vehicle.truck_image,
        trip.vehicle.trailer_image, 
        trip.vehicle.good_transit_licence,
        driver.driver_photo,
        driver.id_img,
        driver.dl_front_img,
        driver.dl_back_img,
        driver.passport_image
    ]

    for document in all_trip_documents:
        # Check the file extension to determine the document type
        file_extension = os.path.splitext(document.name)[1].lower()

        if file_extension == ".pdf":
            # If the document is already a PDF, add it directly to the merger
            pdf_reader = PdfReader(open(document.path, 'rb'))
            merger.append(pdf_reader)
        elif file_extension in (".png", ".jpg", ".jpeg"):
            # If the document is an image (PNG or JPG), convert it to PDF using PIL
            image = Image.open(document.path)
            pdf_buffer = io.BytesIO()
            image.save(pdf_buffer, "PDF")
            pdf_buffer.seek(0)

            # Create a temporary PDF file for the converted image
            temp_pdf_path = f"temp_image.pdf"
            with open(temp_pdf_path, "wb") as temp_pdf_file:
                temp_pdf_file.write(pdf_buffer.read())

            # Open the temporary PDF and add it to the merger
            pdf_reader = PdfReader(open(temp_pdf_path, 'rb'))
            merger.append(pdf_reader)
            
            # Remove the temporary PDF file
            os.remove(temp_pdf_path)

    # Save the merged PDF to a file or send it by email
    merged_pdf_path = f"merged_trip_documents.pdf"
    merger.write(open(merged_pdf_path, 'wb'))
    merger.close()



    #send email
    context = {
        'company':company.name,
        'shipper':shipper.name,
        
    }
    send_email_with_attachment_task(
        context=context, 
        template_path='trip/trip/trip-docs-email.html', 
        from_name=company.name, 
        from_email=company.email, 
        subject="All Trip Documents", 
        recipient_email=shipper.email, 
        replyto_email=company.email,
        attachment_path=merged_pdf_path,  # Attach the merged PDF doc
    )

    messages.success(request, 'Documents sent to the shipper successfully')
    return redirect('view_trip', trip.id)