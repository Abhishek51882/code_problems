from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView
from .models import *
from django.contrib import messages
from django.db.models import Q
import sys
import csv
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .decorators import student_required,teacher_required
@login_required
@teacher_required
def teacher_view(request):
    return render(request,'teacher/teacher.html')
@login_required
@student_required
def test(request):
    items = problem_detail.objects.all()
    context = {
        'items': items,
    }
    if request.method=="POST":
        srch=request.POST['srh']
        if srch:
            match=problem_detail.objects.filter(Q(difficulty__iexact=srch))
            if match:
                return render(request,'problems/test.html',{'sr':match})
            else:
                messages.error(request,'No result found')
        else:
            return HttpResponseRedirect('student/')

    return render(request, 'problems/test.html', context)

def info(request):
    if request.method=="POST":
        srch=request.POST['asg']
        key=request.POST['xxx']
        key=int(key)
        ass=problem_detail.objects.get(pk=key)
        print(ass.name)
        if srch:
            match=problem_detail.objects.filter(Q(name__iexact=srch))
            if match:
                return render(request,'problems/info.html',{'sr':match,"ass":ass})
            else:
                messages.error(request,'No result found')
        else:
            return HttpResponseRedirect('/info/')


    return render(request,'problems/info.html')


def subcode(request):
    if request.method == 'POST':


        code_part = request.POST['code_area']
        key=request.POST['hid']
        key=key.strip()
        key=int(key)

        i = problem_detail.objects.get(pk=key)
        user_name=request.POST['user']

        Que_name=i.name
        searching=Response.objects.filter(Q(name=user_name)&Q(question=Que_name)&Q(status="pass"))
        if searching:
            return HttpResponse("<h1>Already done</h1>")

        blunder1=""
        blunder2=""


        def input():
            a = i.input1

            return a
        try:
            orig_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')
            exec(code_part)
            sys.stdout.close()
            sys.stdout=orig_stdout
            output = open('file.txt', 'r').read()
        except Exception as e:
            sys.stdout.close()
            sys.stdout=orig_stdout
            output = str(e).strip()
            blunder1+=str(e).strip()
        print('first output',output,type(output))
        x=[]
        x.append(output)

        def input():
            a = (i.input2)

            return a
        try:
            orig_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')
            exec(code_part)
            sys.stdout.close()
            sys.stdout=orig_stdout
            output = open('file.txt', 'r').read()
        except Exception as e:
            sys.stdout.close()
            sys.stdout=orig_stdout
            output = str(e).strip()
            blunder2+=str(e).strip()
        print('second output',output,type(output))
        x.append(output)
        b=[]
        for e in x:
            b.append(e.strip())
        print('is is strip of user')
        print(b)
        b2=[]
        y1=i.output1.replace('\r',' ')
        y2=i.output2.replace('\r',' ')
        b2.append(y1)
        b2.append(y2)
        print(b2)


        r=Response()
        flag=0

        if b[0]==blunder1:
            x=blunder1
            flag=1
            res = render(request,'problems/sub.html',{"code":code_part,"output":x,"flag":flag})
            return res
        elif  b[1]==blunder2:
            x=blunder2
            flag=1
            res = render(request,'problems/sub.html',{"code":code_part,"output":x,"flag":flag})
            return res
        elif b[0]==b2[0] and b[1]==b2[1]:
            x="Congrats testcases pass"
            r.status="pass"
            r.marks=2

        else:
            x="Try again"
            r.status="fail"
            r.marks=0

        r.submittion="Submitted"
        r.user_user=request.POST['user']
        r.user_id=request.POST['id']
        r.ass_ass=i.name
        r.ass_id=i.no
        r.name=request.POST['user']
        r.code=request.POST['code_area']
        r.question=i.name


        r.save()

    res = render(request,'problems/sub.html',{"code":code_part,"output":x,"flag":flag})
    return res

def result(request):
    user=request.user
    print(user.id)
    verma=Response.objects.filter(Q(name__icontains=user))
    print(verma)
    return render(request,'problems/result.html',{'user':user,'verma':verma})
def ques(request):
    prob1=problem_detail.objects.all()
    if request.method=='POST':
        prob=problem_detail()
        prob.no=request.POST['no']
        prob.name=request.POST['name']
        prob.difficulty=request.POST['difficulty']
        prob.info=request.POST['info']
        prob.que=request.POST['question']
        prob.input1=request.POST['input1']
        prob.input2=request.POST['input2']
        prob.output1=request.POST['output1']
        prob.output2=request.POST['output2']
        prob.save()
        return render(request,'teacher/statements.html',{'prob':prob1})
    else:
        return render(request,'teacher/ques.html')
def submittion(request):
    sub=Response.objects.all()
    if request.method=='POST':
        name=request.POST['abhi']
        exp=Response.objects.filter(Q(name__icontains=name) | Q(question__icontains=name) | Q(status__icontains=name) )

        return render(request,'teacher/submittion.html',{'sub':exp})

    return render(request,'teacher/submittion.html',{'sub':sub})
def stat(request):
    prob=problem_detail.objects.all()
    return render(request,'teacher/statements.html',{'prob':prob})
def deleteQue(request,id):
    print(id)

    x=problem_detail.objects.filter(name=id)
    x.delete()
    prob=problem_detail.objects.all()
    return render(request,'teacher/statements.html',{'prob':prob})
def edit_que(request,id):
    x=problem_detail.objects.get(name=id)
    fields={'no':x.no,'name':x.name,'difficulty':x.difficulty,'info':x.info,'que':x.que,'input1':x.input1,'input2':x.input2,'output1':x.output1,'output2':x.output2}
    return render(request,'teacher/edit.html',fields)
def final(request):
    fin=request.POST['imp']
    x=problem_detail.objects.get(no=fin)
    x.no=request.POST['no']
    x.name=request.POST['name']
    x.difficulty=request.POST['difficulty']
    x.info=request.POST['info']
    x.que=request.POST['question']
    x.input1=request.POST['input1']
    x.input2=request.POST['input2']
    x.output1=request.POST['output1']
    x.output2=request.POST['output2']
    x.save()
    x=problem_detail.objects.all()
    return render(request,'teacher/statements.html',{'prob':x})
def code(request,id):
    print(id)
    x=Response.objects.get(id=id)
    return render(request,'problems/view_code.html',{'x':x})
def export(request):
    response=HttpResponse(content_type='text/csv')
    writer=csv.writer(response)
    writer.writerow(['no','name','ass','submittion','status','marks','code'])
    for members in Response.objects.all().values_list('id','name','question','submittion','status','marks','code'):
        writer.writerow(members)
    response['Content-Disposition']='attachment;filename="members.csv"'
    return response
def teacher_view_code_fun(request,id):
    print(id)
    x=Response.objects.get(id=id)
    return render(request,'teacher/teacher_view_code.html',{'x':x})
def analysis(request):

        if request.method=='POST':
            name=request.POST['ab']
            s=Response.objects.filter(Q(name__icontains=name)).filter(status='pass').count()
            f=Response.objects.filter(Q(name__icontains=name)).filter(status='fail').count()
            total=Response.objects.filter(Q(name__icontains=name)).count()
            total_pb=problem_detail.objects.count()
            attempts_percent=str(int((s*100)/total))+"%"
            percent_asg=str(int((s*100)/total_pb))+"%"
            marks=2*s
            return render(request,'teacher/analysis.html',{'sum':s,'fail':f,'marks':marks,'ap':attempts_percent,'ac':percent_asg,'name':name})
        return render(request,'teacher/analysis.html')
