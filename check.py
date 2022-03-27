from main import *
USER_ID=1
def exportDeck():
    result=exportDeckAsync.delay()
    return result.wait()
@celery.task()
def exportDeckAsync():
    check_user = User.query.filter_by(id=USER_ID).first()
    decks = check_user.decks
    if len(decks) == 0:
        abort(401, message="No deck found")
    # open the file in the write mode
    filename = "static/temp/"+str(USER_ID)+"-decks.csv"
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        header = ['id', 'name', 'average_score', 'last_review_time','user_id']
        writer.writerow(header)

        # write multiple rows
        for deck in decks:
            d = [deck.id, deck.name, deck.average_score, deck.last_review_time,deck.user_id]
            writer.writerow(d)
        link = "/"+filename
        return jsonify({"link": link})
