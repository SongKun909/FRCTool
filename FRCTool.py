from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML 模板：内嵌了 CSS 进行简单美化
html_template = """
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <title>帧数与时间转换工具</title>
    <style>
      body { 
          font-family: Helvetica, sans-serif; 
          background-color: #f0f0f0; 
          padding: 20px; 
      }
      .container { 
          background-color: #ffffff; 
          padding: 20px; 
          border-radius: 8px; 
          max-width: 400px; 
          margin: auto; 
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      }
      h2 { 
          text-align: center; 
          color: #007acc;
      }
      label { 
          display: block; 
          margin-top: 10px; 
          color: #333;
      }
      input[type="text"] { 
          width: 100%; 
          padding: 8px; 
          margin-top: 5px;
          box-sizing: border-box; 
          border: 1px solid #ccc; 
          border-radius: 4px;
      }
      button { 
          width: 100%; 
          padding: 10px; 
          margin-top: 20px;
          background-color: #007acc; 
          color: #fff; 
          border: none; 
          border-radius: 4px; 
          font-size: 16px;
          cursor: pointer;
      }
      button:hover { 
          background-color: #005f99; 
      }
      .result { 
          margin-top: 20px; 
          font-size: 18px; 
          text-align: center; 
          color: #333; 
      }
      .error {
          color: red;
          text-align: center;
          margin-top: 20px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h2>帧数与时间转换工具</h2>
      <form method="post">
        <label for="fps">FPS (1秒的帧数):</label>
        <input type="text" id="fps" name="fps" value="{{ fps }}">
        <label for="frames">需要转换的帧数:</label>
        <input type="text" id="frames" name="frames" value="{{ frames }}">
        <button type="submit">转换</button>
      </form>
      {% if result %}
      <div class="result">{{ result }}</div>
      {% endif %}
      {% if error %}
      <div class="error">{{ error }}</div>
      {% endif %}
    </div>
  </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    fps = request.form.get("fps", "24")
    frames = request.form.get("frames", "24")
    result = ""
    error = ""
    if request.method == "POST":
        try:
            fps_val = float(fps)
            if fps_val <= 0:
                error = "FPS 必须大于0"
            else:
                frames_val = float(frames)
                if frames_val < 0:
                    error = "帧数不能为负数"
                else:
                    seconds = frames_val / fps_val
                    milliseconds = seconds * 1000
                    result = f"{frames_val} 帧 ≈ {seconds:.5f} 秒  ≈ {milliseconds:.5f} 毫秒"
        except ValueError:
            error = "请输入有效的数字"
    return render_template_string(html_template, fps=fps, frames=frames, result=result, error=error)

if __name__ == "__main__":
    # 生产环境下可取消 debug 参数
    app.run(debug=True)
