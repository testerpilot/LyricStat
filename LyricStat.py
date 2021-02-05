import argparse
import lyricsgenius
import syllables
import shutil
from collections import Counter
import os
import io

genius = lyricsgenius.Genius("API_Key_Goes_Here")
genius.remove_section_headers = True
genius.excluded_terms = ["(Remix)", "(Live)", "(Snippet)"]

# Processes statistics on Lyrics by removing symbols from text,
# counting the syllables of each individual word,  and writing this info
# to a dat file.s
def proccessLyrics(name, verbose):
    inFile = open(name, 'r')
    
    data = inFile.read()

    inFile.close()

    lines = data.splitlines()
    total_line = 0
    count_line = 0
    total_song = num_lines = count_song = 0
    ave_per_line = []
    words = []
    
    for line in lines:
        line = line.lower()
        line = line.replace('?', '')
        line = line.replace('!', '')
        line = line.replace(',', '')
        line = line.replace('?', '')
        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace('*', '')

        line_split = line.split()
        for word in line_split:
            total_line += syllables.estimate(word)
            count_line += 1
            words.append(word)

        if(count_line != 0):
            ave_per_line.append(total_line / count_line)
            total_song += total_line
            num_lines += 1
            count_song += count_line

        count_line = 0
        total_line = 0

    
    average_word = total_song / count_song
    average_line = total_song / num_lines

    dataOut = open(name+".dat", 'w')

    dataOut.write(str(len(ave_per_line))+'\n')
    
    for x in range(0, len(ave_per_line)):
        dataOut.write(str(ave_per_line[x])+'\n')
        
        if verbose == True:
            print("Average syllables on line ", x+1, ":  ", ave_per_line[x])


    dataOut.write(str(average_word)+'\n')
    dataOut.write(str(average_line)+'\n')
    dataOut.write(str(len(Counter(words)))+'\n')

    if verbose:
        print("\nAverage number of syllables per word: ", average_word)
        print("\nAverage number of syllables per line: ", average_line)
            
        print("Num of unique words:  ", len(Counter(words)))

def main():
    inLoop = True
    verbose = False

    parser = argparse.ArgumentParser()
    parser.add_argument("--v", help="Verbose mode", action="store_true")
    args = parser.parse_args()

    if args.v:
        verbose = True

    print("LyricStat 0.1\n")
    
    while(inLoop == True):
        print("\nSelect an option:")
        print("\n1: Download and process a song.")
        print("2: Delete an artist")
        print("3: Delete an song from artist")
        print("4: Exit Program")

        prompt = int(input("\nSelection:  "))

        if prompt == 1:
            name = input("Input name for artist: ")
            song_name = input("Input name for song: ")

            outFile = (song_name+'.txt')
            
            # if artist folder does not exist, create a new one
            if name not in os.listdir():
                os.mkdir(name)

            # change current directory to the artist folder
            os.chdir(os.getcwd()+'/'+name)

            # if lyrics are not already downloaded
            if outFile not in os.listdir():
                song = genius.search_song(song_name, name)
                song.to_text(outFile)
            else:
                prompt = input("Lyrics already in folder for inputted song! Continue download? (yes or no): ")

                if(prompt.lower() == 'yes'):
                    song = genius.search_song(song_name, name)
                    song.to_text(outFile)

            #  process the lyrics and revert back to base directory
            proccessLyrics(outFile, verbose)
            os.chdir("..")

        elif prompt == 2:
            name = input("Input name of artist:  ")
            
            try:
                shutil.rmtree(os.getcwd()+'/'+name)
            except:
                print("Artist does not have an entry to delete")
            
        elif prompt == 3:
            name = input("Input name of artist:  ")
            song_name = input("Input name for song:  ")

            if name not in os.listdir():
                print(name, "does not have a folder")
            else:
                # change the current directory to the artist's folder
                os.chdir(os.getcwd()+'/'+name)

                if song_name+".txt" not in os.listdir():
                    print(song_name, "does not have an entry. Aborting !")
                else:
                    # remove the song and the dat file associated with it
                    os.remove(os.getcwd()+'/'+song_name+".txt")
                    os.remove(os.getcwd()+'/'+song_name+".txt.dat")

                    print(song_name, "by", name, "has been deleted.")

                os.chdir("..")
        elif prompt == 4:
            inLoop = False

    return 0
   
main()
