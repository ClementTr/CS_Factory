from flask import Flask, render_template, redirect, jsonify, request
from factory import Factory
from robot import Robot
from launcher import launch_robot
import threading
import time

global cs_factory
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        main()
        return render_template('home.html')
    return render_template('home.html')


@app.route('/api', methods=['GET', 'POST'])
def api():
    jsonResp = cs_factory.get_stock()
    return jsonify(jsonResp)

def main():
    #Launch 2 first robots
    launch_robot(cs_factory, 2)

    # Wait for all threads to complete
    for rt in cs_factory.robots:
        rt.join()
        print("Stopping " + rt.name)
    print ("Exiting Main Thread")

    # Buy last robots
    cs_factory.final_buy()
    cs_factory.activate_step("Step6", "Work Achieved !!")

if __name__ == '__main__':
    # Create Factory
    cs_factory = Factory(100, 10)
    app.run(debug=True, host="0.0.0.0")
