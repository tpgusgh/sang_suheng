from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
import os
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/")
def main():
    try:
        # SVG 파일 경로
        svg = './map.svg'
        if not os.path.exists(svg):
            return {"error": f"파일 '{svg}'을 찾을 수 없습니다. 경로를 확인하세요."}

        # SVG 파일 읽기
        with open(svg, 'r') as f:
            soup = BeautifulSoup(f, 'xml')
            paths = soup.findAll('path')

        # 채우기 색상
        colors = ['#F1EEF6', '#D4B9BA', '#C993C7', '#DF65B0', '#DD1C77', '#980043']

        # 경로에 색상 스타일 추가
        for i, path in enumerate(paths):
            color_index = i % len(colors)
            path['style'] = f'fill: {colors[color_index]}'

        # 수정된 SVG를 메모리에서 반환
        modified_svg = str(soup)
        return Response(content=modified_svg, media_type='image/svg+xml')

    except FileNotFoundError:
        return {"error": "SVG 파일을 찾을 수 없습니다."}
    except Exception as e:
        return {"error": f"알 수 없는 오류가 발생했습니다: {str(e)}"}
