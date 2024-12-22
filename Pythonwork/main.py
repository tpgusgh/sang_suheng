from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/")
def main():
    try:
        svg = './map.svg'
        if not os.path.exists(svg):
            return {"error": f"파일 '{svg}'을 찾을 수 없습니다. 경로를 확인하세요."}

        with open(svg, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            paths = soup.findAll('path')  


        colors = ['#F1EEF6', '#D4B9BA', '#C993C7', '#DF65B0', '#DD1C77', '#980043']

        total_paths = len(paths)
        color_bins = len(colors)

        for i, path in enumerate(paths):
            color_index = i % color_bins
            color = colors[color_index]  
            path['style'] = f'fill: {color}' 

        modified_svg_path = './modified_map.svg'
        with open(modified_svg_path, 'w') as f:
            f.write(str(soup))

        return FileResponse(modified_svg_path, media_type='image/svg+xml')

    except Exception as e:
        return {"error": f"알 수 없는 오류가 발생했습니다: {str(e)}"}
