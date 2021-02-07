import json
import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.contrib import auth
from webapp.models import RoomBooking,MeetingRoom,UserInfo
from webapp.forms import RegForm

def register(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.cleaned_data.pop("r_password")
            UserInfo.objects.create_user(**form_obj.cleaned_data)
            return redirect('/login/')
    return render(request, 'register.html', locals())


def login(request):
    error = ''
    if request.method == "POST":
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        user = auth.authenticate(username=username, password=pwd)
        if user:
            auth.login(request, user)
            request.session['user'] = username
            return redirect("/index/")
        else:
            error = 'The username or password is not correct.'
    return render(request, "login.html",locals())


def index(request):
    # Validate the user session
    user = request.session.get('user')
    if not user:
        return redirect('/login/')

    date = datetime.datetime.now().date()

    book_date = request.GET.get("book_date", date)
    time_choices = RoomBooking.time_choices
    room_list = MeetingRoom.objects.all()

    book_list = RoomBooking.objects.filter(date=book_date)

    htmls = ""
    for room in room_list:
        htmls += "<tr><td>{}({})</td>".format(room.caption, room.num)
        for time_choice in time_choices:
            book = None
            flag = False
            for book in book_list:
                if book.room.pk == room.pk and book.time_id == time_choice[0]:
                    flag = True
                    break
            if flag:
                if request.user.pk == book.user.pk:
                     htmls += "<td class='active item'  room_id={} time_id={}>{}</td>".format(room.pk, time_choice[0], 'Booked')
                else:
                     htmls += "<td class='another_active item'  room_id={} time_id={}>{}</td>".format(room.pk, time_choice[0], book.user.username)
            else:
                 htmls += "<td room_id={} time_id={} class='item'></td>".format(room.pk, time_choice[0])
        htmls += "</tr>"
    return render(request, "index.html", locals())


def book(request):
    post_data = json.loads(request.POST.get("post_data"))   # {"ADD":{"1":["5"],"2":["5","6"]},"DEL":{"3":["9","10"]}}
    choose_date = request.POST.get("choose_date")
    res = {"state": True, "msg": None}
    try:
        # Add booking
        book_list = []
        for room_id, time_id_list in post_data["ADD"].items():
            for time_id in time_id_list:
                book_obj = RoomBooking(user=request.user, room_id=room_id, time_id=time_id, date=choose_date)
                book_list.append(book_obj)
        RoomBooking.objects.bulk_create(book_list)
        # Delete booking
        for room_id, time_id_list in post_data["DEL"].items():
            for time_id in time_id_list:
                RoomBooking.objects.filter(user=request.user, room_id=room_id, time_id=time_id, date=choose_date).delete()
    except Exception as e:
        res["state"] = False
        res["msg"] = str(e)

    return HttpResponse(json.dumps(res))


def logout(request):
    request.session.clear()
    return redirect('/login/')


def mybooking(request):
    book_list = RoomBooking.objects.filter(user=request.user)
    return render(request, 'mybooking.html', locals())
