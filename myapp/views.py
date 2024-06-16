# myapp/views.py

import io
import fitz  # PyMuPDF
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm
from .models import Resume

def extract_details_from_pdf(file_obj):
    try:
        # Open the PDF file
        pdf_document = fitz.open(file_obj)
        
        # Extract text from each page
        text = ""
        for page_num in range(len(pdf_document)):
            text += pdf_document[page_num].get_text()
        
        # Implement PDF parsing logic to extract details
        name = extract_name(text)
        phone_number = extract_phone_number(text)
        email = extract_email(text)
        years_of_experience = extract_years_of_experience(text)
        skills = extract_skills(text)

        return name, phone_number, email, years_of_experience, skills

    except Exception as e:
        raise ValueError(f'Error parsing PDF file: {str(e)}')

def extract_name(text):
    # Example: Extracting name using regex pattern
    pattern = r'Name:\s*(\w+\s+\w+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''

def extract_phone_number(text):
    # Example: Extracting phone number using regex pattern
    pattern = r'Phone(?:\s*|[\s|.|:]*)Number:\s*([0-9]{3}-[0-9]{3}-[0-9]{4})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''

def extract_email(text):
    # Example: Extracting email using regex pattern
    pattern = r'Email(?:\s*|[\s|.|:]*)ID:\s*(\S+@\S+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''

def extract_years_of_experience(text):
    # Example: Extracting years of experience using regex pattern
    pattern = r'Years(?:\s*|[\s|.|:]*)of(?:\s*|[\s|.|:]*)Experience:\s*([\d.]+)'
    match = re.search(pattern, text)
    if match:
        return float(match.group(1))
    return 0.0

def extract_skills(text):
    # Example: Extracting skills using regex pattern
    pattern = r'Skills:\s*(.*)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''

def upload_resume(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = request.FILES.get('resume')
            if not resume_file:
                messages.error(request, 'No file chosen. Please select a PDF file.')
                return redirect('upload_resume')

            # Handle PDF file
            if resume_file.name.endswith('.pdf'):
                try:
                    name, phone_number, email, years_of_experience, skills = extract_details_from_pdf(resume_file)
                except ValueError as e:
                    messages.error(request, str(e))
                    return redirect('upload_resume')
            else:
                messages.error(request, 'Unsupported file format. Please upload a PDF file.')
                return redirect('upload_resume')

            # Save extracted details to the database
            resume = Resume(
                name=name,
                phone_number=phone_number,
                email=email,
                years_of_experience=years_of_experience,
                skills=skills
            )
            resume.save()
            messages.success(request, 'Resume uploaded successfully.')
            return redirect('resume_list')
    else:
        form = UploadFileForm()
    return render(request, 'upload_resume.html', {'form': form})

def resume_list(request):
    resumes = Resume.objects.all()
    return render(request, 'resume_list.html', {'resumes': resumes})
