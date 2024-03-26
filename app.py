from flask import Flask, render_template, request
import webbrowser
import time

app = Flask(__name__, template_folder='templates')



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        meeting_link = request.form["meeting_link"]
        join_time_str = request.form["join_time"]

        # Validate and split the input into hours and minutes
        try:
            hours, minutes = map(int, join_time_str.split(":"))
            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                raise ValueError("Hours and minutes out of range")
        except (ValueError, IndexError):
            message = "Invalid time format or out-of-range values."
        else:
            join_time = time.mktime((2023, 9, 17, hours, minutes, 0, -1, -1, -1))
            message = join_zoom_meeting(meeting_link, join_time)

        return render_template("index.html", message=message)

    return render_template("index.html", message=None)


def join_zoom_meeting(meeting_link, join_time):
    current_time = time.time()
    wait_time = join_time - current_time

    if wait_time > 0:
        print(f"Waiting for {wait_time:.1f} seconds...")
        time.sleep(wait_time)

    webbrowser.open(meeting_link)
    print("Joined the Zoom meeting!")


if __name__ == '__main__':
    app.run()