!pip install google-generativeai --quiet
!pip install ipywidgets --quiet  #for a beautiful ui
import google.generativeai as genai
import ipywidgets as widgets
from IPython.display import display,Markdown
API_KEY="AIzaSyBquXkJ1oFMintfSkqg3ES8b6V-MLkNiwQ"
genai.configure(api_key=API_KEY)
model=genai.GenerativeModel("gemini-2.5-flash")


topic_input=widgets.Text(
    description="Topic",
    layout = widgets.Layout(width="400px")
)

tone_input=widgets.Dropdown(
    description="Tone",
    options=['professional','casual','witty',]
)

submit_button = widgets.Button(
    description="Submit",
    button_style = "Success",
    tooltip = "click to generate tweet",
    layout = widgets.Layout(width = "400px")
    )




output = widgets.Output()



def generate_tweet(b):
  output.clear_output()
  prompt = f"""
  your a comedian who always tells jokes in reverse string
  """
  with output:
    try:
      response=model.generate_content(prompt)
      tweet=response.text.strip()
      display(Markdown(f"###Genetare tweet:\n\n{tweet}"))
    except Exception as e:
      print("error",e)

submit_button.on_click(generate_tweet)
form = widgets.VBox([
    widgets.HTML(value="<h3> Tweet Generator Agent</h3>"),
    topic_input,
    submit_button,
    output,

])


display(form)


