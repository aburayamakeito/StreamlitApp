import time
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import patheffects


def init():
  fig = plt.figure(figsize=(8,8), facecolor='white', dpi=200)
  ax = fig.add_subplot(111)
  return fig, ax


def draw_style(fig, ax):
  ax.spines['bottom'].set_position('zero')
  ax.spines['left'].set_position('zero')
  fig.gca().yaxis.set_ticks_position('left')
  fig.gca().xaxis.set_ticks_position('bottom')
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)

  ax.set_xlim(-10, 10)
  ax.set_ylim(-10, 10)

  # # 主目盛：刻み間隔2、0は非表示、文字を白縁取り
  ax.set_xticks(np.arange(-10, 10 + 1, 1))
  labels = ax.set_xticklabels([(x if x != 0 and x % 2 == 0 else '') for x in np.arange(-10, 10 + 1, 1)])
  for t in labels:
    t.set_path_effects([patheffects.Stroke(linewidth=3, foreground='white'), patheffects.Normal()])

  ax.set_yticks(np.arange(-10, 10 + 1, 1))
  labels = ax.set_yticklabels([(y if y != 0 and y % 2 == 0 else '') for y in np.arange(-10, 10 + 1, 1)])
  for t in labels:
    t.set_path_effects([patheffects.Stroke(linewidth=3, foreground='white'), patheffects.Normal()])

  ax.tick_params(which='major', direction='inout', length=5)

  # # 補助目盛（minor）：刻み間隔1でグリッド描画するための準備
  ax.set_xticks(np.linspace(-10, 10, 1), minor=True)
  ax.set_yticks(np.linspace(-10, 10, 1), minor=True)
  ax.tick_params(which='minor', direction='inout', length=5)

  # # グリッド（which='both'で、majorとminorの目盛位置にグリッド）
  ax.grid(which='both')
  return fig, ax

def make_data_fig(fig, ax, make=True, a=0, b=0, mark=True):
  if make:
    ax.cla()
    x = np.linspace(-100, 100, 1000)
    y = float(a) * x + float(b)
    ax.plot(x, y)
    if b != 0 and a != 0 and mark:
      ax.plot(-(float(b)/float(a)), 0, marker='o')
    if mark:
      ax.plot(0, b, marker='o')
    fig, ax = draw_style(fig, ax)
    return fig, ax
  else:
    ax.cla()
    x = np.linspace(-100, 100, 1000)
    ax.plot(x, x)
    ax.plot(0, 0, marker='o')
    fig, ax = draw_style(fig, ax)
    return fig, ax


def create_domain(ax, a, b, small, large, check=True):
  try:
    if check:
      small_x = float(small)
      large_x = float(large)
      small_y = round(float(a) * float(small) + float(b), 1)
      large_y = round(float(a) * float(large) + float(b), 1)
      
    if not check:
      small_y = float(small)
      large_y = float(large)
      small_x = round((float(small) - float(b)) / float(a), 1)
      large_x = round((float(large) - float(b)) / float(a), 1)
  except ZeroDivisionError:
    return ax, 0, 0
  x = np.linspace(float(small_x), float(large_x), 1000)
  y = float(a) * x + float(b)
  x_small_line = np.linspace(0, small_x, 1000)
  x_large_line = np.linspace(0, large_x, 1000)
  y_small_line = np.linspace(0, small_y, 1000)
  y_large_line = np.linspace(0, large_y, 1000)
  small_x_full = np.full(1000, small_x)
  large_x_full = np.full(1000, large_x)
  small_y_full = np.full(1000, small_y)
  large_y_full = np.full(1000, large_y)
  ax.plot(x, y, color='red')
  ax.plot(small_x_full, y_small_line, color="red", linestyle="--")
  ax.plot(large_x_full, y_large_line, color="red", linestyle="--")
  ax.plot(x_small_line, small_y_full, color="red", linestyle="--")
  ax.plot(x_large_line, large_y_full, color="red", linestyle="--")
  if check:
    return ax, small_y, large_y
  else:
    return ax, small_x, large_x

def start_domain(plot_fig, fig, ax, speed=0, a=0, b=0, small=0, large=0):
  roop = True
  speed = int(speed)
  x = float(small)
  while roop:
    fig, ax = make_data_fig(fig, ax, True, a, b, False)
    create_domain(ax, a, b, small, large, True)
    y = float(a) * x + float(b)
    ax.plot(x, y, color="blue", marker='o')
    line_x = np.linspace(float(small), float(x), 1000)
    ax.plot(line_x, float(a) * line_x + float(b), color='green')
    x = round(0.1 + x, 1)
    
    plot_fig.pyplot(fig)
    time.sleep(1/speed)
    if x > float(large):
        break


# ----------------------------------------------------------------------------- #


fig, ax = init()
left_btn_y_bool = False
right_btn_y_bool = False
start = False
a=0
b=0
roop = False

# サイドバー
item = st.sidebar.selectbox('公式',('一次関数 y=ax+b', '選択肢2', '選択肢3'))


if item == '一次関数 y=ax+b':
  a = st.sidebar.text_input('傾きa：', a)
  if type(a) is str:
    try:
      a = eval(a)
    except SyntaxError:
      pass
  a = st.sidebar.slider('a', -10.0, 10.0, float(a), 0.1, "%.1f")
  b = st.sidebar.text_input('切片b：', b)
  if type(b) is str:
    try:
      b = eval(b)
    except SyntaxError:
      pass
  b = st.sidebar.slider('b', -10.0, 10.0, float(b), 0.1, "%.1f")
  st.sidebar.write('-'*30)
  
  check = st.sidebar.checkbox('変域')
  
  if check:
    domain = st.sidebar.radio('軸', ('X の変域', 'Y の変域'))
    st.sidebar.write('変域値')
    left_entry_domain, right_entry_domain = st.sidebar.beta_columns(2)
    entry_small = left_entry_domain.text_input('small', '-1')
    entry_large = right_entry_domain.text_input('large', '1')
    left_btn_y, right_btn_y = st.sidebar.beta_columns(2)
    if domain == 'X の変域':
      fig, ax = make_data_fig(fig, ax, True, a, b, False)
      x_small = entry_small
      x_large = entry_large
      ax, y_small, y_large = create_domain(ax, a, b, entry_small, entry_large, True)
    if domain == 'Y の変域':
      y_small = entry_small
      y_large = entry_large
      fig, ax = make_data_fig(fig, ax, True, a, b, False)
      ax, x_small, x_large = create_domain(ax, a, b, entry_small, entry_large, False)

    left_y, right_y = st.sidebar.beta_columns(2)
    x = left_y.latex(f'{x_small} ≦ X ≦ {x_large}')
    y = right_y.latex(f'{y_small} ≦ Y ≦ {y_large}')
    
    left_domain_value, right_domain_start = st.sidebar.beta_columns(2)
    domain_speed = left_domain_value.slider('スピード（s⁻¹）', 1, 100, 1, 1, "%d")
    domain_speed = right_domain_start.number_input('スピード（s⁻¹）', min_value=1, max_value=100, value=domain_speed)
    start = st.sidebar.button("スタート")

  if not check:
    fig, ax = make_data_fig(fig, ax, True, a, b)


# メイン画面
st.title('DrawingTools')
if a == 0 and b == 0:
  st.latex('y = x')
else:
  st.latex('y = {}x + {}'.format(str(a), str(b)))
if check and (left_btn_y_bool or right_btn_y_bool):
  st.latex(f'変域：{x_small} ≦ X ≦ {x_large}')
plot_fig = st.pyplot(fig)

if start:
  start_domain(plot_fig, fig, ax, domain_speed, a, b, x_small, x_large)

