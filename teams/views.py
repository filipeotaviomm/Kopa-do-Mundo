from rest_framework.views import APIView, Response, Request, status
from teams.models import Team
from django.forms.models import model_to_dict
from utils import data_processing
from exceptions import (
  NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError
  )


class TeamView(APIView):
    def post(self, request: Request) -> Response:
        try:
            data_processing(request.data)
            team = Team.objects.create(**request.data)
            return Response(model_to_dict(team), status.HTTP_201_CREATED)
        except (
            NegativeTitlesError,
            InvalidYearCupError,
            ImpossibleTitlesError
        ) as error:
            return Response(
                {"error": error.message}, status.HTTP_400_BAD_REQUEST
            )

    def get(self, request: Request) -> Response:
        team_dict = [model_to_dict(team) for team in Team.objects.all()]
        return Response(team_dict, status.HTTP_200_OK)


class TeamIdView(APIView):
    def get(self, request, team_id: int) -> Response:
        try:
            team_found = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status.HTTP_404_NOT_FOUND
            )
        return Response(model_to_dict(team_found), status.HTTP_200_OK)

    def patch(self, request, team_id: int) -> Response:
        try:
            team_found = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status.HTTP_404_NOT_FOUND
            )
        for key, value in request.data.items():
            setattr(team_found, key, value)
        # o setattr faz esse processo abaixo com os todos os campos
        # team_account.name = request.data.get("name", found_account.name)
        team_found.save()
        return Response(model_to_dict(team_found), status.HTTP_200_OK)

    def delete(self, request, team_id: int) -> Response:
        try:
            team_found = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status.HTTP_404_NOT_FOUND
            )
        team_found.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
