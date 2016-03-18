from uta_models.models import Qualification
from operator import add
import numpy as np


class Matching:
    def __init__(self, groups, requirements, student):
        self.dim = Qualification.objects.count()
        self.groups = groups
        # Keep only the groups that are not full of members
        self.groups = [g for g in groups if len(g.students.all()) < requirements.max_group_size]

        self.all_qualifs = []
        for qualif in Qualification.objects.all():
            self.all_qualifs.append(str(qualif.name))
        # print self.all_qualifs

        self.rated_qualif_requirements_vector = self.create_ndim_qualif_vector(requirements.rated_qualifications.all(),
                                                                               False)
        self.student_rated_qualif_vector = self.create_ndim_qualif_vector(student.rated_qualifications.all())

    def rank(self):
        # Compute the aggregated group qualification vectors
        group_scores = self.compute_group_scores(self.groups)

        # Compute benefit foreach group
        benefits = [self.compute_benefit(g) for g in group_scores]

        # Map primary keys to their benefits -> (group, benefit)
        zipped = zip(self.groups, benefits)

        # Sort tuples by second argument -> benefit
        return sorted(zipped, key=lambda x: x[1], reverse=True)

    def compute_group_scores(self, groups):
        groups_scores = []

        for group in groups:
            sum_vector = np.zeros((self.dim,), dtype=np.int)

            for student in group.students.all():
                sum_vector = map(add, sum_vector, self.create_ndim_qualif_vector(student.rated_qualifications))

            groups_scores.append(sum_vector)

        return groups_scores

    def create_ndim_qualif_vector(self, rated_qualifications, filter=True):
        qualif_vector = np.zeros((self.dim,), dtype=np.int)

        for rated_qualif in rated_qualifications.all():
            index = self.all_qualifs.index(rated_qualif.qualification.name)
            if filter:
                # Filter by requirements
                if self.rated_qualif_requirements_vector[index] == 0:
                    qualif_vector[index] = 0
                else:
                    qualif_vector[index] = rated_qualif.rating
            else:
                qualif_vector[index] = rated_qualif.rating

        return qualif_vector

    def compute_benefit(self, group_scores):
        benefit = 0

        for index in range(0, len(group_scores)):
            r = self.rated_qualif_requirements_vector[index]
            s = self.student_rated_qualif_vector[index]
            g = group_scores[index]

            #if g+s > r then benefit = r-g
            benefit += min(r, g + s) - g

        return benefit
