def start_read(source_file):
    with open(source_file,"r") as f:
        record=f.read()
        return record

def move(m):
    M="" #rendered_move
    capture=0
    #castle
    if(m.lower()=="ooo" or m.lower()=="oo"):
        M='-'.join(m.upper()) #https://stackoverflow.com/a/3258612/8235105
        return M
    else: #fix later, it should not be needed
        if(m[0].lower()!="x"):
            past=m[0:2]
            present=m[-2:len(m)]
            piece=m[2:-2]
        else:
            past=m[1:3]
            present=m[-2:len(m)]
            piece=m[3:-2]
            capture=1
        #rendering the move:
        pt=piece[0] #piece type
        if(pt.lower()=="p"):
            M=f"{past[0]}x{present}" if(capture) else f"{present}"
        else:
            M=f"{pt.upper()}{past}x{present}" if(capture) else f"{pt.upper()}{past}{present}" #remove upper() if needed
        return M


def decode_stringhistory(record):
    #orders moves
    record_listed=record.split(" - ")
    record_listed[-1]=record_listed[-1][:-1]
    if(record_listed[-1]==""):
        record_listed.pop()
    record_ordered=""
    for i,m in enumerate(record_listed):
        iteration=i//2+1
        Blackstate=i%2
        if(not Blackstate):
            record_ordered+=f"{iteration}. "
        processed_move=move(m)
        record_ordered+=f"{processed_move} " #move
    return record_ordered

def to_pgn():
    #moves source file
    source="chess-pgn.txt"
    #record
    record=start_read(source)
    PGNrecord="""[Event "Hoogovens Group A"]
    [Site "Wijk aan Zee NED"]
    [Date "1999.01.20"]
    [EventDate "1999.01.16"]
    [Round "4"]
    [Result "1-0"]
    [White "Garry Kasparov"]
    [Black "Veselin Topalov"]
    [ECO "B07"]
    [WhiteElo "2812"]
    [BlackElo "2700"]
    [PlyCount "87"]

    """
    result=decode_stringhistory(record)
    PGNrecord+=result
    import time
    timestr = time.strftime("%H:%M:%S-%d+%m+%y")
    fname=f"PGN{timestr}.txt"
    with open(fname,"w+") as f:
        f.write(PGNrecord)
    return 0
