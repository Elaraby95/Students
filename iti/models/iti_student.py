from odoo import models, fields, api
from odoo.exceptions import UserError


class ItiStudent(models.Model):
    _name = "iti.student"
    # _rec_name ='level'

    name = fields.Char(required=True, string="My Name")
    email = fields.Char()
    birth_date = fields.Date()
    salary = fields.Float()
    tax = fields.Float(compute="calc_tax")
    address = fields.Text()
    gender = fields.Selection(
        [('m', "male"), ('f', "female")]
    )
    accepted = fields.Boolean()
    color = fields.Integer()
    level = fields.Integer()
    image = fields.Binary()
    cv = fields.Html()
    login_time = fields.Datetime()
    track_id = fields.Many2one("iti.track")
    track_capacity = fields.Integer(related="track_id.capacity")
    skill_id = fields.Many2many("iti.skill")
    grade_ids = fields.One2many("student.course.line", "students_id")
    state = fields.Selection([
        ('applied', 'Applied'),
        ('first', 'First interview'),
        ('second', 'Second interview'),
        ('passed', 'Passed'),
        ('rejected', 'Rejected'),
    ], default='applied')



    def set_first(self):
        self.state = 'first'

    def set_second(self):
        self.state = 'second'

    def set_rejected(self):
        self.state = 'rejected'

    def set_passed(self):
        self.state = 'passed'

    def set_back(self):
        if self.state in ['passed', 'rejected']:
            self.state = 'applied'

    @api.depends("salary")
    def calc_tax(self):
        for ahmed in self:
            ahmed.tax = ahmed.salary * .02

    @api.model
    def create(self, vals):
        if vals["salary"] > 10000:
            raise UserError("salary can't be greater than 10000")
        name_split = vals['name'].split()
        vals["email"] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        search_student = self.search([('email', '=', vals['email'])])
        if search_student:
            raise UserError("Email Already Exist")
        return super().create(vals)

    def write(self, vals):
        if "salary" in vals and vals["salary"] > 10000:
            raise UserError("salary can't be greater than 10000")
        if "name" in vals:
            name_split = vals["name"].split()
            vals["email"] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
            search_student = self.search([('email', '=', vals['email'])])
            if search_student:
                raise UserError("Email Already Exist")
        super().write(vals)

    def unlink(self):
        for record in self:
            if record.state in ['passed', 'rejected']:
                raise UserError("You can't delete passed/rejected students")
        super().unlink()

    @api.constrains("track_id")
    def check_track_id(self):
        track_count = len(self.track_id.student_ids)
        track_capacity = self.track_id.capacity
        if track_count > track_capacity:
            raise UserError("track is full")

    @api.onchange("gender")
    def saw(self):
        if not self.gender:
            return {}
        elif self.gender == 'm':
            self.salary = 10000
        else:
            self.salary = 5000
        return {
            'warning': {
                'title': 'hello',
                'message': 'you have changed the gender'
            }
        }


class ItiCourse(models.Model):
    _name = 'iti.course'

    name = fields.Char()


class StudentCourseGrades(models.Model):
    _name = "student.course.line"

    students_id = fields.Many2one("iti.student")
    course_id = fields.Many2one("iti.course")
    grade = fields.Selection([
        ("g", "good"),
        ("vg", "very good"),
    ])
