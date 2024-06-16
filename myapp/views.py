import fitz  # PyMuPDF
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm
from .models import Resume
from django.db.models import Q

def extract_details_from_pdf(file_obj):
    try:
        # Open the PDF file
        pdf_document = fitz.open(stream=file_obj.read(), filetype="pdf")
        
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
    pattern = r'Name:\s*(\w+\s+\w+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return 'Unknown'

def extract_phone_number(text):
    pattern = r'Phone(?:\s*|[\s|.|:]*)Number:\s*([0-9]{3}-[0-9]{3}-[0-9]{4})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return 'Unknown'

def extract_email(text):
    pattern = r'Email(?:\s*|[\s|.|:]*)ID:\s*(\S+@\S+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return 'Unknown'

def extract_years_of_experience(text):
    pattern = r'Years(?:\s*|[\s|.|:]*)of(?:\s*|[\s|.|:]*)Experience:\s*([\d.]+)'
    match = re.search(pattern, text)
    if match:
        return float(match.group(1))
    return 0.0

def extract_skills(text):
    pattern = r'Skills:\s*(.*)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return 'Unknown'

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
    skill_filter = request.GET.get('skill', '')
    sort_by_experience = request.GET.get('sort', '')

    resumes = Resume.objects.all()

    if skill_filter:
        resumes = resumes.filter(skills__icontains=skill_filter)

    if sort_by_experience == 'asc':
        resumes = resumes.order_by('years_of_experience')
    elif sort_by_experience == 'desc':
        resumes = resumes.order_by('-years_of_experience')

    return render(request, 'resume_list.html', {
        'resumes': resumes,
        'skill_filter': skill_filter,
        'sort_by_experience': sort_by_experience
    })