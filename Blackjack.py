# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = [0, 0, 0 ,0]
covered = [0]
cvalue = ["..."]

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# draw card back 
def draw_back(canvas, pos):
    card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * 0, CARD_CENTER[1] + CARD_SIZE[1]*covered[0])
    canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []
        self.hand_ranks = []
    def __str__(self):
        return "Hand contains " + string_list_join(self.hand)	# return a string representation of a hand

    def add_card(self, card):
        self.hand.append(card.suit + card.rank)
        self.hand_ranks.append(card.rank)
        self.strhand = string_list_join(self.hand)   
        
    def get_value(self): 
# count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust        
        m = 0               
        for i in self.hand_ranks:
            m+= VALUES.get(i) 	  
        if "A" in self.hand_ranks and m<=11: 
            m+=10    
        return m
    
    def draw(self, canvas, pos):
        for i in range(len(self.hand)):
            column = pos[0] + 100 * i
            card = Card(self.hand[i][0], self.hand[i][-1])
            card.draw(canvas, [column, pos[1]])
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append(i+j)
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        self.card = Card(self.deck[-1][0],self.deck[-1][1])	# deal a card object from the deck
        self.card_dealt = self.deck.pop()
        return self.card
    def __str__(self):
        return 	"Deck contains " + string_list_join(self.deck)  # return a string representing the deck     


#define string+list functions
def string_list_join(string_list):
    ans = ""
    for i in range(len(string_list)):
        ans += string_list[i] + " "
    return ans
    
        

#define event handlers for buttons
def deal():
    global outcome, in_play, myhand, comphand, deck, bust_it
    covered[0] = 0
    cvalue[0] = "..."
    if in_play == True:
        score[1]+=1
        score[2]+=1 	
        outcome = "You gave up this round!"
    else:
        outcome = "New deal! Hit or stand?"
    in_play = True
    deck = Deck()
    deck.shuffle()
    comphand = Hand()
    myhand = Hand()

    for i in range (2):
        myhand.add_card(deck.deal_card())
        comphand.add_card(deck.deal_card())
    print ""
    print "Deck:" + str(deck)
    print "Comp hand: " + str(comphand)
    print "Value: " + str(comphand.get_value())
    print "Ma hand: " + str(myhand)
    print "Value: " + str(myhand.get_value())

    
def hit():
    global in_play, outcome
    if in_play == True:
        covered[0] = 0
        myhand.add_card(deck.deal_card())
        if myhand.get_value() < 21:
            print ""
            print "Deck: " + str(deck)
            print "Comp hand: " + str(comphand)
            print "Value: " + str(comphand.get_value())
            print "Ma hand: " + str(myhand)
            print "Value: " + str(myhand.get_value())
            outcome = "Hit or stand?"

        elif myhand.get_value() > 21:
            print ""
            print "Deck: " + str(deck)
            print "Comp hand: " + str(comphand)
            print "Value: " + str(comphand.get_value())
            print "Ma hand: " + str(myhand)
            print "Value: " + str(myhand.get_value())
            print ""
            print "BUSTED"
            outcome = "You are busted... New deal?"
            in_play = False
            score[1]+=1
            score[2]+=1
            cvalue[0] = str(comphand.get_value())
            covered[0] = 1

        else:
            print ""
            print "Deck: " + str(deck)
            print "Comp hand: " + str(comphand)
            print "Value: " + str(comphand.get_value())
            print "Ma hand: " + str(myhand)
            print "Value: " + str(myhand.get_value())
            #print ""
            print "LUCKY DEVIL"
            outcome = "WOW! Blackjack!"
            
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global in_play, outcome
    if in_play == False:
        cvalue[0] = str(comphand.get_value())
        if outcome == "Busted":
            print "Busted"
            outcome = "You are busted start anew.."
            covered[0] = 1
    else:
        cvalue[0] = str(comphand.get_value())
        while comphand.get_value() < 17:
            comphand.add_card(deck.deal_card())
        cvalue[0] = str(comphand.get_value())
        if comphand.get_value() > 21:
            print ""
            print "Deck: " + str(deck)
            print "Comp hand: " + str(comphand)
            print "Value: " + str(comphand.get_value())
            print "Ma hand: " + str(myhand)
            print "Value: " + str(myhand.get_value())
            outcome = "Dealer is Busted! YOU WON!"
            print "Enemy Busted "
            score[0]+=1
            score[3]+=1
            covered[0] = 1
        elif myhand.get_value() > comphand.get_value():
            print ""
            print "Deck: " + str(deck)
            print "Comp hand: " + str(comphand)
            print "Value: " + str(comphand.get_value())
            print "Ma hand: " + str(myhand)
            print "Value: " + str(myhand.get_value())
            outcome = "You are WINNER! New deal?"
            print "Yo WINNER"
            score[0]+=1
            score[3]+=1
            covered[0] = 1
        else:
            print ""
            print "Deck: " + str(deck)
            print "Comp hand: " + str(comphand)
            print "Value: " + str(comphand.get_value())
            print "Ma hand: " + str(myhand)
            print "Value: " + str(myhand.get_value())
            outcome = "Dealer wins! New deal?"
            print "Comp wins"
            score[1]+=1
            score[2]+=1
            covered[0] = 1
    in_play = False                # replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    myhand.draw(canvas, [0, 500])
    comphand.draw(canvas, [0, 0])
    canvas.draw_text("Your hit: " + str(myhand.get_value()), [400, 410], 24, "Black")
    canvas.draw_text("Dealer hit: " + cvalue[0], [400, 180], 24, "Black")
    canvas.draw_text(outcome, [170, 270], 24, "Black")
    canvas.draw_text("Wins/Losses: " + str(score[0])+"/" +str(score[1]), [400, 440], 24, "Black")
    canvas.draw_text("Wins/Losses: " + str(score[2])+"/" +str(score[3]), [400, 150], 24, "Black")
    canvas.draw_text("Blackjack v1.0", [525, 595], 12, "Black")
    draw_back(canvas, [0, 0])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric