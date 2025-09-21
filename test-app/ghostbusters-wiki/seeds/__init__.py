from app import db
from models import Ghost

def seed_ghosts():
    ghosts = [
        Ghost(name="Slimer"),
        Ghost(name='Zuul')
    ]

    for ghost in ghosts:
        db.session.add(ghost)

    db.session.commit()

if __name__ == "__main__":
    print("This is the seeds folder")