from flask import render_template, request, redirect, jsonify
import gizeh
import moviepy.editor as mp
from moviepy.video.tools.credits import credits1

def lvs_vg_ctr():
    if request.method == 'POST':
        try:
            credits = request.form['credits']
            if credits:
                BASE_PATH = '/home/Admingania/portal_gain/ai_services/lite_video_generation/static/'
                TEXTS_PATH = BASE_PATH + 'texts/'
                # Save the text
                filename_text = 'text.txt'
                with open(TEXTS_PATH + filename_text, 'w') as f:
                    f.write(credits)
                # Generate the video
                width = 1280
                clip = credits1(TEXTS_PATH + filename_text, width=width)

                scrolling_credits = clip.set_pos(lambda t:('center',-10*t))
                final_clip = mp.CompositeVideoClip([scrolling_credits])
                # Save the file
                VIDEOS_PATH = BASE_PATH + 'videos/'
                filename_gen = 'credits.mp4'
                final_clip.set_duration(10).subclip(2,20).write_videofile(VIDEOS_PATH + filename_gen, fps=24)
                # clip.set_pos(lambda t:('center',-10*t)).set_duration(10).write_videofile(VIDEOS_PATH + filename_gen, fps=24)
                # Serve final video file
                return render_template('lvs_index.html', video_file=filename_gen, controls=True)
        except Exception as e:
            return jsonify({'error': f'Error: {e}'}), 400
    else:
        return render_template('lvs_index.html', controls=True)







import numpy as np

def generate_ctr_gol():
    # Get the details from the form
    duration = 5  # shorter duration
    width = 100  # smaller width
    height = 100  # smaller height
    bg_color = "#000000"  # fixed black background color request.form['bg_color']

    # Create the initial grid randomly
    grid = np.random.randint(2, size=(height, width))

    # Define the rules for the game of life
    def iterate_game_of_life(grid):
        # Calculate the number of neighbors for each cell
        neighbors_count = sum(np.roll(np.roll(grid, i, axis=0), j, axis=1)
                              for i in (-1, 0, 1) for j in (-1, 0, 1)
                              if (i != 0 or j != 0))
        # Apply the rules
        new_grid = np.logical_or(np.logical_and(grid, neighbors_count == 2),
                                 neighbors_count == 3).astype(int)
        return new_grid

    # Define the function that returns the current frame as a MoviePy clip
    def make_frame(t):
        nonlocal grid
        # Update the grid for the current frame
        for _ in range(3):
            grid = iterate_game_of_life(grid)
        # Create the Gizeh surface and draw the grid
        surface = gizeh.Surface(width, height, bg_color=None)
        dot_radius = min(width, height) / (max(width, height) * 100)
        for i in range(height):
            for j in range(width):
                if grid[i, j] == 1:
                    x = (j + 0.5) * width / float(width)
                    y = (i + 0.5) * height / float(height)
                    gizeh.circle(dot_radius, xy=(x, y)).draw(surface)
        return surface.get_npimage()

    # Create the MoviePy clip and set the duration
    clip = mp.VideoClip(make_frame, duration=duration)

    # Return the clip as a response
    BASE_PATH = '/home/Admingania/portal_gain/ai_services/lite_video_generation/static/videos/'
    clip.write_videofile(BASE_PATH + 'output.mp4', fps=24)
    return redirect('video')


def generate_ctr():
    # Get the details from the form
    duration = int(request.form['duration'])
    width = int(request.form['width'])
    height = int(request.form['height'])
    bg_color = "#000000"  # fixed black background color request.form['bg_color']
    text = request.form['text']

    # Create the Gizeh surface and draw the text
    surface = gizeh.Surface(width, height, bg_color=None)
    text_color = (1, 1, 1) # White text
    text_size = height * 0.1 # 10% of the height
    gizeh.text(text, fontfamily='Arial', fontsize=text_size, fill=text_color, xy=(width/2, height/2)).draw(surface)

    # Create the MoviePy clip and set the duration
    clip = mp.VideoClip(lambda t: surface.get_npimage(), duration=duration)
    clip.fps=24
    # Return the clip as a response
    BASE_PATH = '/home/Admingania/portal_gain/ai_services/lite_video_generation/static/videos/'
    clip.write_videofile(BASE_PATH + 'output.mp4')
    return redirect('video')

def video_ctr():
    return render_template('video.html')
