from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from app.api.database.base import Base

# Define a UserRoles association table to manage many-to-many relationship between users and roles
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)


# User Account Management
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    password = Column(String(300))
    active = Column(Boolean)
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    certificates = relationship("Certificate", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    images = relationship("Images", back_populates="user")
    replies = relationship("CommentReply", back_populates="user")
    education = relationship("Education", back_populates="user")
    experience = relationship("Experience", back_populates="user")
    project = relationship("Project", back_populates="user")
    # Add other user-related fields as needed


# Role model
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)
    users = relationship("User", secondary=user_roles, back_populates="roles")


# Certificate
class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(10))
    description = Column(String(200))
    date_issued = Column(DateTime)
    issuer = Column(String(50))
    user = relationship("User", back_populates="certificates")


# Comment
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    text = Column(String(500))
    timestamp = Column(DateTime)
    user = relationship("User", back_populates="comments")
    replies = relationship("CommentReply", back_populates="comment")
    project = relationship("Project", back_populates="comments")


# Images
class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    image_url = Column(String(50))
    description = Column(String(200))
    timestamp = Column(DateTime)
    user = relationship("User", back_populates="images")
    project = relationship("Project", back_populates="images")
    # details = relationship("Images", back_populates="image")


# CommentReply
class CommentReply(Base):
    __tablename__ = "comment_replies"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String(500))
    timestamp = Column(DateTime)
    comment = relationship("Comment", back_populates="replies")
    user = relationship("User", back_populates="replies")


# Education
class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    degree = Column(String(50))
    institution = Column(String(50))
    completion_date = Column(DateTime)
    user = relationship("User", back_populates="education")


# Experience
class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(100))
    organization = Column(String(100))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    user = relationship("User", back_populates="experience")


# ImageDetails
# class ImageDetails(Base):
#     __tablename__ = "image_details"
#     id = Column(Integer, primary_key=True, index=True)
#     details = Column(String)
#     image_id = Column(Integer, ForeignKey("images.id"))
#     image = relationship("Images", back_populates="image_details")


# Ministries
class Ministry(Base):
    __tablename__ = "ministries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(200))
    contact_info = Column(String(100))


# ProjectAgreement
class ProjectAgreement(Base):
    __tablename__ = "project_agreements"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    amount = Column(Float)
    project = relationship("Project", back_populates="agreements")


# ProjectPaymentReceipts
class ProjectPaymentReceipts(Base):
    __tablename__ = "project_payment_receipts"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    payment_id = Column(Integer, ForeignKey("project_payments.id"))
    description = Column(String(200))
    project = relationship("Project", back_populates="receipts")
    payments = relationship("ProjectPayments", back_populates="receipt")


# ProjectPayments
class ProjectPayments(Base):
    __tablename__ = "project_payments"

    id = Column(Integer, primary_key=True, index=True)
    payment_method = Column(String(50))
    payment_date = Column(DateTime)
    amount = Column(Float)
    receipt = relationship("ProjectPaymentReceipts", back_populates="payments")


# Projects
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    description = Column(String(200))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    budget = Column(Float)
    status = Column(String(200))
    user_id = Column(Integer, ForeignKey("users.id"))
    ministry_id = Column(Integer, ForeignKey("ministries.id"))

    # Define relationships with various user roles for the project
    user = relationship("User", secondary="project_contractors", back_populates="project")

    # Other relationships with certificates, comments, images, agreements, receipts, and published

    comments = relationship("Comment", back_populates="project")
    images = relationship("Images", back_populates="project")
    agreements = relationship("ProjectAgreement", back_populates="project")
    receipts = relationship("ProjectPaymentReceipts", back_populates="project")
    published = relationship("Published", back_populates="project")
    contracts = relationship("Contract", back_populates='project')


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True, unique=True, nullable=False)
    details = Column(String(500))  # Add the details field
    # Define other fields as needed

    # Relationships
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="contracts")


class ProjectContractors(Base):
    __tablename__ = "project_contractors"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    contractor_id = Column(Integer, ForeignKey("users.id"))


# Published
class Published(Base):
    __tablename__ = "published"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    timestamp = Column(DateTime)
    project = relationship("Project", back_populates="published")
