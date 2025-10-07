from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(75), unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(30), nullable=False)
    username = Column(String(50), unique=True, nullable=False)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    following = relationship("Follower", foreign_keys="[Follower.user_from_id]", back_populates="user_from")
    followers = relationship("Follower", foreign_keys="[Follower.user_to_id]", back_populates="user_to")


class Post(db.Model):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    media = relationship("Media", back_populates="post")


class Comment(db.Model):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    comment_text = Column(String(500), nullable=False)

    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="comments")

    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    post = relationship("Post", back_populates="comments")


class Media(db.Model):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    type = Column(Enum("image", "video", name="media_types"), nullable=False)
    url = Column(String(250), nullable=False)

    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    post = relationship("Post", back_populates="media")


class Follower(db.Model):
    __tablename__ = "follower"

    id = Column(Integer, primary_key=True) 
    user_from_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_to_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user_from = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    user_to = relationship("User", foreign_keys=[user_to_id], back_populates="followers")
