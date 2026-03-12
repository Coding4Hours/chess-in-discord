import chess
import chess.svg
from fastapi import FastAPI, HTTPException, Response, Query

app = FastAPI()


@app.get("/api/moves/{moves_str}")
async def get_chess_board(
    moves_str: str,
):
    moves = [m.strip() for m in moves_str.split(",") if m.strip()]

    board = chess.Board()
    last_move = None
    try:
        for move_text in moves:
            last_move = board.push_san(move_text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid move: {str(e)}")

    board_view = board.turn

    board_svg = chess.svg.board(
        board=board,
        lastmove=last_move,
        orientation=board_view,
        size=400,
        check=board.king(board.turn) if board.is_check() else None,
    )

    return Response(
        content=board_svg,
        media_type="image/svg+xml",
        headers={"Cache-Control": "public, max-age=3600"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
