# -------------------------#
# ---Program by MiVainer---#
def connecting():
    conn = sqlite3.connect("database.db")
    return conn


@bot.message_handler(commands=['dist'])
def dist(message):
   conn = connecting()
   cursor = conn.cursor()
   cursor.execute("SELECT id FROM orders")
   results = cursor.fetchall()
   for result in results:
       bot.send_message(result[0], message_to_send) # в message_to_send передайте текст любым удобным для вас способом
   conn.close()