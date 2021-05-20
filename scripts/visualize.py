import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import ScalarFormatter

total = pd.read_json(
    "/Users/bene/Desktop/dataset2/captured/TOTAL_create-dataset/total_filtered.json")

html = pd.read_json(
    "/Users/bene/Desktop/dataset2/captured/create-dataset_html/create-dataset.com/filtered.json")

css = pd.read_json(
    "/Users/bene/Desktop/dataset2/captured/create-dataset_css/create-dataset.com/filtered.json")

js = pd.read_json(
    "/Users/bene/Desktop/dataset2/captured/create-dataset_js/create-dataset.com/filtered.json")

sess = pd.read_json(
    "/Users/bene/Desktop/dataset2/captured/create-dataset_session-variable/create-dataset.com/filtered.json")

facebook = pd.read_json(
    "/Users/bene/Desktop/dataset2/captured/create-dataset_facebook/create-dataset.com/filtered.json")

twitter = pd.read_json(
    "/Users/bene/Desktop/dataset2/captured/create-dataset_twitter/create-dataset.com/filtered.json")

google = pd.read_json(
    "/Users/bene/Desktop/dataset2/captured/create-dataset_google/create-dataset.com/filtered.json")

canvas = pd.read_json(
    "/Users/bene/Desktop/dataset2/captured/create-dataset_canvas-fingerprinting/create-dataset.com/filtered.json")

#  get 15 first rows of the data
# print(df.head(15))

# print information about the data
# print(df.info())

# delete frame number from dataframe
# del html["frame.number"]

# print(html.info())

# get numbers of tracker in html
# print(len(html[html.tracker == 'true']))


# PLOTTING
# bar plot number of packets and distribution tcp/udp/trackers
def dataset_total():
    total_len = len(total)
    total_tcp = total.tcp.count()
    total_udp = total.udp.count()
    total_tracker = len(total[total.tracker == 'true'])

    labels = ["Synthetischer Datensatz"]

    x = np.arange(len(labels))

    width = 0.25

    # 1 color=(0.71, 0.76, 0.86)
    # 2 color=(0.49, 0.6, 0.78)
    # 3 color=(0.235, 0.39, 0.58)
    # 4 color=(0.6, 0.53, 0.64)

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - 1.5*width, total_len,
                    width, label='Datenpakete gesamt', color=(0.71, 0.76, 0.86))
    rects2 = ax.bar(x-width/2, total_tcp, width, label='TCP-Pakete',
                    color=(0.49, 0.6, 0.78))
    rects3 = ax.bar(x+width/2, total_udp, width,
                    label='UDP-Pakete', color=(0.235, 0.39, 0.58))

    rects4 = ax.bar(x + 1.5*width, total_tracker, width,
                    label='Tracker', color=(0.6, 0.53, 0.64))

    rects5 = ax.bar(x + 2.5*width, 0, width)

    rects6 = ax.bar(x + 3.5*width, 0, width)

    # rects7 = ax.bar(x + 4.5*width, 0, width)

    ax.set_ylabel('Anzahl Datenpakete')

    ax.set_title('Verteilung der Datenpakete')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # ax.bar_label(rects0, padding=1)

    ax.bar_label(rects1, padding=1)
    ax.bar_label(rects2, padding=1)
    ax.bar_label(rects3, padding=1)
    ax.bar_label(rects4, padding=1)
    # ax.bar_label(rects5, padding=1)
    # ax.bar_label(rects6, padding=1)
    # ax.bar_label(rects7, padding=1)
    fig.tight_layout()

    plt.yscale('symlog', linthreshy=100)

    ax.yaxis.set_major_formatter(ScalarFormatter())
    plt.ylim(0, 3000)
    plt.show()


# dataset_total()


def dataset_split_barplot():

    html_tracker = 0
    css_tracker = 0
    js_tracker = 0
    sess_tracker = len(sess[sess.tracker == 'true'])
    facebook_tracker = len(facebook[facebook.tracker == 'true'])
    twitter_tracker = len(twitter[twitter.tracker == 'true'])
    google_tracker = len(google[google.tracker == 'true'])
    canvas_tracker = len(canvas[canvas.tracker == 'true'])

    html_len = len(html)
    html_tcp = html.tcp.count()
    html_udp = html.udp.count()

    css_len = len(css)
    css_tcp = css.tcp.count()
    css_udp = css.udp.count()

    js_len = len(js)
    js_tcp = js.tcp.count()
    js_udp = js.udp.count()

    sess_len = len(sess)
    sess_tcp = sess.tcp.count()
    sess_udp = sess.udp.count()

    facebook_len = len(facebook)
    facebook_tcp = facebook.tcp.count()
    facebook_udp = facebook.udp.count()

    twitter_len = len(twitter)
    twitter_tcp = twitter.tcp.count()
    twitter_udp = twitter.udp.count()

    google_len = len(google)
    google_tcp = google.tcp.count()
    google_udp = google.udp.count()

    canvas_len = len(canvas)
    canvas_tcp = canvas.tcp.count()
    canvas_udp = canvas.udp.count()

    labels = ["HTML", "CSS", "JS", "Session Variable",
              "Facebook", "Twitter", "Google", "Fingerprinting"]

    # HTML / CSS / JS / SESSION_VARIABLE / FACEBOOK / TWITTER / GOOGLE / CANVAS FINGERPRINTING
    packets_total = [html_len, css_len, js_len, sess_len,
                     facebook_len, twitter_len, google_len, canvas_len]
    tcp_packets = [html_tcp, css_tcp, js_tcp, sess_tcp,
                   facebook_tcp, twitter_tcp, google_tcp, canvas_tcp]
    udp_packets = [html_udp, css_udp, js_udp, sess_udp,
                   facebook_udp, twitter_udp, google_udp, canvas_udp]

    tracker_packets = [html_tracker, css_tracker, js_tracker, sess_tracker,
                       facebook_tracker, twitter_tracker, google_tracker, canvas_tracker]

    # label locations
    x = np.arange(len(labels))

    width = 0.2

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - width, packets_total,
                    width, label='Datenpakete gesamt', color=(0.71, 0.76, 0.86))
    rects2 = ax.bar(x, tcp_packets, width, label='TCP-Pakete',
                    color=(0.49, 0.6, 0.78))
    rects3 = ax.bar(x + width, udp_packets, width,
                    label='UDP-Pakete', color=(0.235, 0.39, 0.58))
    rects4 = ax.bar(x + 2*width, tracker_packets, width,
                    label='Tracker', color=(0.6, 0.53, 0.64))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Anzahl Datenpakete')
    ax.set_title('Aufteilung des Datensatz')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding=1)
    ax.bar_label(rects2, padding=1)
    ax.bar_label(rects3, padding=1)
    ax.bar_label(rects4, padding=1)

    fig.tight_layout()

    plt.yscale('symlog', linthreshy=25)

    ax.yaxis.set_major_formatter(ScalarFormatter())
    plt.ylim(0, 2000)
    plt.show()


dataset_split_barplot()


def plot_tracker():

    html_tracker = 0
    css_tracker = 0
    js_tracker = 0
    sess_tracker = len(sess[sess.tracker == 'true'])
    facebook_tracker = len(facebook[facebook.tracker == 'true'])
    twitter_tracker = len(twitter[twitter.tracker == 'true'])
    google_tracker = len(google[google.tracker == 'true'])
    canvas_tracker = len(canvas[canvas.tracker == 'true'])

    labels = ["HTML", "CSS", "JS", "Session Variable",
              "Facebook", "Twitter", "Google", "Fingerprinting"]

    # HTML / CSS / JS / SESSION_VARIABLE / FACEBOOK / TWITTER / GOOGLE / CANVAS FINGERPRINTING
    tracker = [html_tracker, css_tracker, js_tracker, sess_tracker,
               facebook_tracker, twitter_tracker, google_tracker, canvas_tracker]
    # tcp_packets = [html_tcp, css_tcp, js_tcp, sess_tcp,
    #                facebook_tcp, twitter_tcp, google_tcp, canvas_tcp]
    # udp_packets = [html_udp, css_udp, js_udp, sess_udp,
    #                facebook_udp, twitter_udp, google_udp, canvas_udp]

    # label locations
    x = np.arange(len(labels))

    width = 0.3

    fig, ax = plt.subplots()

    rects1 = ax.bar(x, tracker,
                    width, label='Tracker-belastete Datenpakete', color=(0.71, 0.76, 0.86))
    # rects2 = ax.bar(x, tcp_packets, width, label='TCP-Pakete',
    #                 color=(0.49, 0.6, 0.78))
    # rects3 = ax.bar(x + width, udp_packets, width,
    #                 label='UDP-Pakete', color=(0.235, 0.39, 0.58))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Anzahl Datenpakete')
    ax.set_title('Verteilung der Tracker-belasteten Datenpakete')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding=1)
    # ax.bar_label(rects2, padding=1)
    # ax.bar_label(rects3, padding=1)

    fig.tight_layout()

    plt.show()


# plot_tracker()